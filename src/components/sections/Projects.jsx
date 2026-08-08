import { useState } from 'react';
import { FileText, Play, X } from 'lucide-react';
import { GithubIcon, VercelIcon } from '../icons/BrandIcons';
import { PROJECTS } from '../../constants/data';

/**
 * Projects Section — Grid of project cards with hover effects.
 * Each card: name, description, tech tags, GitHub + Vercel + Video + Docs buttons.
 */
export default function Projects() {
  const [activeVideo, setActiveVideo] = useState(null);

  return (
    <div role="region" aria-label="Projects">
      <h2 className="text-2xl font-bold text-text-primary">Projects</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {PROJECTS.map((project) => (
          <article
            key={project.name}
            className="group rounded-lg border border-border bg-bg-card p-5 transition-all duration-250 hover:border-accent hover:shadow-[0_0_20px_rgba(59,130,246,0.15)] hover:-translate-y-1 flex flex-col justify-between"
          >
            <div>
              <h3 className="text-base font-semibold text-text-primary group-hover:text-accent transition-colors duration-250">
                {project.name}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-text-secondary">
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
            </div>

            {/* Action buttons */}
            <div className="mt-5 flex flex-wrap items-center gap-2.5">
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

              {project.video && (
                <button
                  onClick={() => setActiveVideo(project.video)}
                  className="inline-flex items-center gap-1.5 rounded border border-accent/40 bg-accent/10 px-2.5 py-1 text-xs font-medium text-accent hover:bg-accent/20 transition-all duration-200 cursor-pointer"
                  aria-label={`Watch ${project.name} Video Demo`}
                >
                  <Play size={12} className="fill-accent" />
                  <span>Working Video</span>
                </button>
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

      {/* Video Modal Player */}
      {activeVideo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
          <div className="relative w-full max-w-4xl rounded-xl border border-border bg-bg-card p-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-border mb-3">
              <h4 className="text-sm font-semibold text-text-primary">Project Demo Video</h4>
              <button
                onClick={() => setActiveVideo(null)}
                className="rounded p-1 text-text-secondary hover:bg-bg-primary hover:text-text-primary transition-colors cursor-pointer"
                aria-label="Close Video Modal"
              >
                <X size={18} />
              </button>
            </div>
            <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-black">
              <video
                src={activeVideo}
                controls
                autoPlay
                className="h-full w-full object-contain"
              >
                Your browser does not support HTML5 video player.
              </video>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
