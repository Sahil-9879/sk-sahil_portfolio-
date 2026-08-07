import { ABOUT } from '../../constants/data';

/**
 * About Section — Professional bio, education timeline, and interests.
 * No progress bars, no charts — clean typography only.
 */
export default function About() {
  return (
    <div className="space-y-8" role="region" aria-label="About Me">
      {/* Bio */}
      <div>
        <h2 className="text-2xl font-bold text-text-primary">About Me</h2>
        <div className="mt-4 space-y-3">
          {ABOUT.bio.map((paragraph, i) => (
            <p
              key={i}
              className="text-sm leading-relaxed text-text-secondary md:text-base"
            >
              {paragraph}
            </p>
          ))}
        </div>
      </div>

      {/* Education Timeline */}
      <div>
        <h3 className="text-lg font-semibold text-text-primary">Education</h3>
        <div className="mt-4 space-y-4">
          {ABOUT.education.map((edu, i) => (
            <div
              key={i}
              className="relative border-l-2 border-border pl-5 py-1"
            >
              {/* Timeline dot */}
              <div className="absolute -left-[5px] top-2.5 h-2 w-2 rounded-full bg-accent" />
              <h4 className="text-sm font-semibold text-text-primary">
                {edu.degree}
              </h4>
              <p className="mt-0.5 text-sm text-accent">{edu.institution}</p>
              <p className="mt-0.5 text-xs font-mono text-text-secondary">
                {edu.period}
              </p>
              <p className="mt-1.5 text-sm text-text-secondary">
                {edu.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Interests */}
      <div>
        <h3 className="text-lg font-semibold text-text-primary">Interests</h3>
        <div className="mt-3 flex flex-wrap gap-2">
          {ABOUT.interests.map((interest) => (
            <span
              key={interest}
              className="rounded border border-border px-3 py-1 text-xs font-mono text-text-secondary"
            >
              {interest}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
