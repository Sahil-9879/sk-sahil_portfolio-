import { NAV_SECTIONS } from '../constants/data';

/**
 * ExpandingNav — The signature interaction of the portfolio.
 *
 * Horizontal navigation where the active tab expands to ~65-70% width
 * while inactive tabs share the remaining space. Uses inline flex styles
 * with CSS transitions for buttery-smooth animation.
 *
 * On mobile: converts to vertical layout preserving the expand concept.
 */
export default function ExpandingNav({ activeSection, onNavigate }) {
  const totalSections = NAV_SECTIONS.length;

  return (
    <div
      className="flex flex-col md:flex-row w-full border border-border rounded-t-lg overflow-hidden"
      role="tablist"
      aria-label="Section navigation"
    >
      {NAV_SECTIONS.map((section, index) => {
        const isActive = activeSection === section;
        const isLast = index === totalSections - 1;

        return (
          <button
            key={section}
            role="tab"
            aria-selected={isActive}
            aria-controls={`panel-${section.toLowerCase().replace(/\s+/g, '-')}`}
            onClick={() => onNavigate(section)}
            className="cursor-pointer border-none relative flex items-center justify-center text-sm font-medium tracking-wide uppercase outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-inset"
            style={{
              flexGrow: isActive ? 5 : 1,
              flexShrink: 1,
              flexBasis: 0,
              padding: '14px 20px',
              backgroundColor: isActive ? '#111827' : '#0F172A',
              color: isActive ? '#3B82F6' : '#94A3B8',
              transition: 'flex-grow 350ms cubic-bezier(0.4, 0, 0.2, 1), background-color 250ms ease, color 250ms ease',
              borderRight: !isLast ? '1px solid #334155' : 'none',
            }}
            onMouseEnter={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = 'rgba(17, 24, 39, 0.6)';
                e.currentTarget.style.color = '#F8FAFC';
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = '#0F172A';
                e.currentTarget.style.color = '#94A3B8';
              }
            }}
          >
            {/* Active indicator — bottom bar on desktop */}
            {isActive && (
              <span
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent"
                style={{
                  boxShadow: '0 0 8px rgba(59,130,246,0.4)',
                }}
                aria-hidden="true"
              />
            )}
            <span className="relative z-10 whitespace-nowrap text-xs md:text-sm select-none">
              {section}
            </span>
          </button>
        );
      })}
    </div>
  );
}
