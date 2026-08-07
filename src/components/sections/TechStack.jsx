import { SKILLS } from '../../constants/data';

/**
 * Tech Stack Section — Categorized skill cards with hover interaction.
 * Hover: blue border, glow, brighter bg, translateY(-4px).
 */
export default function TechStack() {
  return (
    <div role="region" aria-label="Tech Stack">
      <h2 className="text-2xl font-bold text-text-primary">Tech Stack</h2>
      <div className="mt-6 space-y-6">
        {Object.entries(SKILLS).map(([category, items]) => (
          <div key={category}>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
              {category}
            </h3>
            <div className="mt-3 flex flex-wrap gap-2">
              {items.map((skill) => (
                <div
                  key={skill}
                  className="rounded border border-border bg-bg-card px-3.5 py-2 text-sm font-medium text-text-primary transition-all duration-250 hover:border-accent hover:bg-bg-card-hover hover:shadow-[0_0_16px_rgba(59,130,246,0.2)] hover:-translate-y-1 cursor-default"
                  role="listitem"
                >
                  {skill}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
