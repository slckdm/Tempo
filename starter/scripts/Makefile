up:
	docker compose -f ../docker-compose.yaml up -d \
	&& docker compose -f ../../management/docker-compose.yaml up -d \
	&& docker compose -f ../../metadata/docker-compose.yaml up -d \
	&& docker compose -f ../../streaming/docker-compose.yaml up -d \
	&& docker compose -f ../../frontend/docker-compose.yaml up -d

up_build:
	docker compose -f ../docker-compose.yaml up --build  -d \
	&& docker compose -f ../../management/docker-compose.yaml up --build -d \
	&& docker compose -f ../../metadata/docker-compose.yaml up --build -d \
	&& docker compose -f ../../streaming/docker-compose.yaml up --build -d \
	&& docker compose -f ../../frontend/docker-compose.yaml up --build -d

down:
	docker compose -f ../docker-compose.yaml down \
	&& docker compose -f ../../management/docker-compose.yaml down \
	&& docker compose -f ../../metadata/docker-compose.yaml down \
	&& docker compose -f ../../streaming/docker-compose.yaml down \
	&& docker compose -f ../../frontend/docker-compose.yaml down
