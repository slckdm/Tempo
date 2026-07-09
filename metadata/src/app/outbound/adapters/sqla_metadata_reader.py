from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types.enum import UploadStatus

from app.core.models.track_metadata import TrackMetadata as table
from app.core.queries.models.list_metadata import ListMetadataQM
from app.core.queries.models.metadata import MetadataQM
from app.core.queries.ports.metadata_reader import FilterParams, MetadataReader, PaginationParams
from app.outbound.exceptions import MetadataReaderError


class SQLAMetadataReader(MetadataReader):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_filter(
        self, filters: FilterParams, pagination: PaginationParams
    ) -> ListMetadataQM:

        where_clause = [table.processing_status == UploadStatus.COMPLETED]
        if filters.title:
            where_clause.append(table.title.ilike(f"%{filters.title}%"))
        if filters.artist:
            where_clause.append(table.artist.ilike(f"%{filters.artist}%"))
        if filters.album:
            where_clause.append(table.album.ilike(f"%{filters.album}%"))
        if filters.genre:
            where_clause.append(table.genre.ilike(f"%{filters.genre}%"))

        query = (
            select(
                table.upload_id,
                table.title,
                table.artist,
                table.album,
                table.genre,
                table.year,
                table.duration,
                table.cover_key,
                table.size,
                table.created_at,
                table.created_by,
                table.processing_status,
                table.filename,
                table.content_type,
                func.count().over().label("total"),
            )
            .where(*where_clause)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )
        try:
            result = await self._session.execute(query)
            rows = result.all()
        except SQLAlchemyError as sqlalchemy_err:
            raise MetadataReaderError from sqlalchemy_err

        if not rows:
            result = await self._session.execute(
                select(func.count().label("total")).where(*where_clause)
            )
            total = result.one().total
            return ListMetadataQM(
                metadata=[], total=total, offset=pagination.offset, limit=pagination.limit
            )

        return ListMetadataQM(
            metadata=[
                MetadataQM(
                    id=row.upload_id,
                    title=row.title,
                    artist=row.artist,
                    album=row.album,
                    genre=row.genre,
                    year=row.year,
                    duration=row.duration,
                    cover_key=row.cover_key,
                    size=row.size,
                    created_at=row.created_at,
                    created_by=row.created_by,
                    processing_status=row.processing_status,
                    filename=row.filename,
                    content_type=row.content_type,
                )
                for row in rows
            ],
            total=rows[0].total,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_by_id(self, id: UUID) -> MetadataQM | None:
        statement = select(
            table.upload_id,
            table.title,
            table.artist,
            table.album,
            table.genre,
            table.year,
            table.duration,
            table.cover_key,
            table.size,
            table.created_at,
            table.created_by,
            table.processing_status,
            table.filename,
            table.content_type,
        ).where(table.upload_id == id)
        try:
            row = (await self._session.execute(statement)).one_or_none()
        except SQLAlchemyError as sqlalchemy_err:
            raise MetadataReaderError from sqlalchemy_err

        return MetadataQM(
            id=row.upload_id,
            title=row.title,
            artist=row.artist,
            album=row.album,
            genre=row.genre,
            year=row.year,
            duration=row.duration,
            cover_key=row.cover_key,
            size=row.size,
            created_at=row.created_at,
            created_by=row.created_by,
            processing_status=row.processing_status,
            filename=row.filename,
            content_type=row.content_type,
        ) if row else None
