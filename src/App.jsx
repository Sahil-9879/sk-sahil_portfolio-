import { useState, useCallback } from 'react';
import Navbar from './components/layout/Navbar';
import Profile from './components/sections/Profile';
import ExpandingNav from './components/ExpandingNav';
import ContentPanel from './components/ContentPanel';
import Terminal from './components/Terminal';

/**
 * App — Root component.
 * Single-page layout: Navbar → Profile → ExpandingNav + ContentPanel.
 * Terminal modal accessible from navbar.
 */
export default function App() {
  const [activeSection, setActiveSection] = useState('About');
  const [terminalOpen, setTerminalOpen] = useState(false);

  const handleNavigate = useCallback((section) => {
    setActiveSection(section);
  }, []);

  const toggleTerminal = useCallback(() => {
    setTerminalOpen((prev) => !prev);
  }, []);

  const closeTerminal = useCallback(() => {
    setTerminalOpen(false);
  }, []);

  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Navbar */}
      <Navbar
        activeSection={activeSection}
        onNavigate={handleNavigate}
        onTerminalToggle={toggleTerminal}
      />

      {/* Profile Section */}
      <Profile />

      {/* Expanding Navigation + Content Panel */}
      <main className="mx-auto max-w-6xl px-6 pb-12">
        <ExpandingNav
          activeSection={activeSection}
          onNavigate={handleNavigate}
        />
        <ContentPanel activeSection={activeSection} />
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-6 text-center">
        <p className="text-xs text-text-secondary font-mono">
          Built with discipline, not templates.
        </p>
      </footer>

      {/* Terminal Modal */}
      <Terminal
        isOpen={terminalOpen}
        onClose={closeTerminal}
        onNavigate={handleNavigate}
      />
    </div>
  );
}
