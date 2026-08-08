import { FileText } from 'lucide-react';
import { GithubIcon, VercelIcon } from '../icons/BrandIcons';
import { PROJECTS } from '../../constants/data';

/**
 * Projects Section — Grid of project cards with hover effects.
 * Each card: name, description, tech tags, GitHub + Vercel + Docs buttons.
 */
export default function Projects() {
  return (
    <div role="region" aria-label="Projects">
      <h2 className="text-2xl font-bold text-text-primary">Projects</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {PROJECTS.map((project) => (
          <article
            key={project.name}
            className="group rounded-lg border border-border bg-bg-card p-5 transition-all duration-250 hover:border-accent hover:shadow-[0_0_20px_rgba(59,130,246,0.15)] hover:-translate-y-1"
          >
            <h3 className="text-base font-semibold text-text-primary group-hover:text-accent transition-colors duration-250">
              {project.name}
            </h3>
            <p className="mt-2 text-sm leading-relaxed text-text-secondary line-clamp-3">
              {project.description}
            </p>

            {/* Tech tags */}
            <div className="mt-3 flex flex-wrap gap-1.5">
              {project.tech.map((t) => (
                <span
                  key={t}
                  className="rounded bg-bg-primary px-2 py-0.5 text-xs font-mono text-text-secondary"
                >
                  {t}
                </span>
              ))}
            </div>

            {/* Action buttons */}
            <div className="mt-4 flex flex-wrap items-center gap-3">
              {project.github && (
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded border border-border bg-bg-primary px-2.5 py-1 text-xs text-text-secondary hover:border-accent hover:text-accent transition-all duration-200"
                  aria-label={`View ${project.name} on GitHub`}
                >
                  <GithubIcon size={12} />
                  <span>GitHub</span>
                </a>
              )}
              {project.demo && (
                <a
                  href={project.demo}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded border border-border bg-bg-primary px-2.5 py-1 text-xs text-text-secondary hover:border-accent hover:text-accent transition-all duration-200"
                  aria-label={`View ${project.name} live on Vercel`}
                >
                  <VercelIcon size={12} />
                  <span>Vercel</span>
                </a>
              )}
              {project.docs && (
                <a
                  href={project.docs}
                  download="Sk_Sahil_Portfolio_Engineering_Guide.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded border border-border bg-bg-primary px-2.5 py-1 text-xs text-text-secondary hover:border-accent hover:text-accent transition-all duration-200"
                  aria-label={`Download ${project.name} Engineering Guide PDF`}
                >
                  <FileText size={12} />
                  <span>Guide PDF</span>
                </a>
              )}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
