import { useState, useCallback } from 'react';
import {
  FileText,
  TerminalSquare,
  Menu,
  X,
} from 'lucide-react';
import { GithubIcon, LinkedinIcon } from '../icons/BrandIcons';
import { PERSONAL } from '../../constants/data';

/**
 * Navbar — Sticky, transparent, with thin bottom border.
 * Contains logo, section links, external links, and terminal toggle.
 */
export default function Navbar({ activeSection, onNavigate, onTerminalToggle }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = ['About', 'Projects', 'Skills', 'Contact'];

  const handleNav = useCallback(
    (section) => {
      const sectionMap = { Skills: 'Tech Stack' };
      onNavigate(sectionMap[section] || section);
      setMobileOpen(false);
    },
    [onNavigate]
  );

  const getLinkClass = (section) => {
    const mapped = section === 'Skills' ? 'Tech Stack' : section;
    const isActive = activeSection === mapped;
    return `text-sm transition-colors duration-200 ${
      isActive
        ? 'text-accent font-medium'
        : 'text-text-secondary hover:text-text-primary'
    }`;
  };

  return (
    <nav
      className="sticky top-0 z-50 border-b border-border bg-bg-primary/90 backdrop-blur-sm"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
        {/* Logo */}
        <a
          href="/"
          className="font-mono text-sm font-medium text-text-primary hover:text-accent transition-colors duration-200"
          aria-label="Home"
        >
          &lt;{PERSONAL.name.toLowerCase()} /&gt;
        </a>

        {/* Desktop Nav */}
        <div className="hidden items-center gap-6 md:flex">
          {navItems.map((item) => (
            <button
              key={item}
              onClick={() => handleNav(item)}
              className={`${getLinkClass(item)} cursor-pointer bg-transparent border-none`}
              aria-label={`Navigate to ${item}`}
            >
              {item}
            </button>
          ))}

          <span className="h-4 w-px bg-border" aria-hidden="true" />

          {/* External Links */}
          <a
            href={PERSONAL.resume}
            download="Sk_Sahil_Resume.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors duration-200"
            aria-label="Download Resume"
          >
            Resume
          </a>
          <a
            href={PERSONAL.github}
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-secondary hover:text-text-primary transition-colors duration-200"
            aria-label="GitHub Profile"
          >
            <GithubIcon size={16} />
          </a>
          <a
            href={PERSONAL.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-secondary hover:text-text-primary transition-colors duration-200"
            aria-label="LinkedIn Profile"
          >
            <LinkedinIcon size={16} />
          </a>

          <span className="h-4 w-px bg-border" aria-hidden="true" />

          {/* Terminal Button */}
          <button
            onClick={onTerminalToggle}
            className="flex items-center gap-1.5 rounded border border-border bg-transparent px-2.5 py-1 text-xs font-mono text-text-secondary hover:border-accent hover:text-accent transition-all duration-200 cursor-pointer"
            aria-label="Open Terminal"
          >
            <TerminalSquare size={14} />
            <span className="hidden lg:inline">Terminal</span>
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="text-text-secondary hover:text-text-primary md:hidden bg-transparent border-none cursor-pointer"
          aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="border-t border-border bg-bg-primary px-6 py-4 md:hidden">
          <div className="flex flex-col gap-3">
            {navItems.map((item) => (
              <button
                key={item}
                onClick={() => handleNav(item)}
                className={`${getLinkClass(item)} text-left cursor-pointer bg-transparent border-none py-1`}
              >
                {item}
              </button>
            ))}
            <hr className="border-border" />
            <a
              href={PERSONAL.resume}
              download="Sk_Sahil_Resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
            >
              <FileText size={14} /> Resume
            </a>
            <a
              href={PERSONAL.github}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
            >
              <GithubIcon size={14} /> GitHub
            </a>
            <a
              href={PERSONAL.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
            >
              <LinkedinIcon size={14} /> LinkedIn
            </a>
            <hr className="border-border" />
            <button
              onClick={() => {
                onTerminalToggle();
                setMobileOpen(false);
              }}
              className="flex items-center gap-2 text-sm font-mono text-text-secondary hover:text-accent bg-transparent border-none cursor-pointer text-left py-1"
            >
              <TerminalSquare size={14} /> Terminal
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
