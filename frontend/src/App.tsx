import { AuthProvider, useAuth } from "./context/AuthContext";
import { LibraryProvider } from "./context/LibraryContext";
import { PlayerProvider } from "./context/PlayerContext";
import { Header } from "./components/Header";
import { LoginScreen } from "./components/LoginScreen";
import { LibraryView } from "./components/LibraryView";
import { PlayerBar } from "./components/PlayerBar";

function Workspace() {
  return (
    <div className="app">
      <Header />
      <main className="main">
        <div className="layout">
          <LibraryView />
        </div>
      </main>
      <PlayerBar />
    </div>
  );
}

function Gate() {
  const { user } = useAuth();
  if (!user) return <LoginScreen />;
  return (
    <LibraryProvider>
      <PlayerProvider>
        <Workspace />
      </PlayerProvider>
    </LibraryProvider>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Gate />
    </AuthProvider>
  );
}
