import { FileText, User } from 'lucide-react';
import { GithubIcon, LinkedinIcon } from '../icons/BrandIcons';
import { PERSONAL } from '../../constants/data';

/**
 * Profile Section — Two-column layout with avatar and info.
 * Clean, no hero background, no animations.
 */
export default function Profile() {
  return (
    <section
      className="mx-auto max-w-6xl px-6 py-12 md:py-16"
      aria-label="Profile"
    >
      <div className="flex flex-col items-center gap-8 md:flex-row md:items-start md:gap-12">
        {/* Avatar */}
        <div className="shrink-0">
          <div className="flex h-32 w-32 items-center justify-center rounded-full border-2 border-border bg-bg-card md:h-40 md:w-40">
            {PERSONAL.avatar ? (
              <img
                src={PERSONAL.avatar}
                alt={`${PERSONAL.name}'s profile`}
                className="h-full w-full rounded-full object-cover"
              />
            ) : (
              <User size={48} className="text-text-secondary" />
            )}
          </div>
        </div>

        {/* Info */}
        <div className="flex-1 text-center md:text-left">
          <h1 className="text-3xl font-bold tracking-tight text-text-primary md:text-4xl">
            {PERSONAL.name}
          </h1>
          <p className="mt-2 text-lg text-accent font-medium">
            {PERSONAL.role}
          </p>
          <p className="mt-1 text-sm text-text-secondary">
            {PERSONAL.college}
          </p>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-text-secondary">
            {PERSONAL.intro}
          </p>

          {/* Action Buttons */}
          <div className="mt-6 flex flex-wrap justify-center gap-3 md:justify-start">
            <a
              href={PERSONAL.resume}
              download="Sk_Sahil_Resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded border border-accent bg-accent/10 px-4 py-2 text-sm font-medium text-accent hover:bg-accent/20 transition-colors duration-200"
              aria-label="Download Resume"
            >
              <FileText size={16} />
              Resume
            </a>
            <a
              href={PERSONAL.github}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded border border-border px-4 py-2 text-sm text-text-secondary hover:border-text-secondary hover:text-text-primary transition-colors duration-200"
              aria-label="GitHub Profile"
            >
              <GithubIcon size={16} />
              GitHub
            </a>
            <a
              href={PERSONAL.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded border border-border px-4 py-2 text-sm text-text-secondary hover:border-text-secondary hover:text-text-primary transition-colors duration-200"
              aria-label="LinkedIn Profile"
            >
              <LinkedinIcon size={16} />
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
