import {
  Mail,
  FileText,
  MapPin,
} from 'lucide-react';
import { GithubIcon, LinkedinIcon } from '../icons/BrandIcons';
import { CONTACT_LINKS } from '../../constants/data';

const ICON_MAP = {
  Mail,
  Github: GithubIcon,
  Linkedin: LinkedinIcon,
  FileText,
  MapPin,
};

/**
 * Contact Section — Grid of contact cards with hover interaction.
 * Same hover pattern as skill cards: blue border, glow, translate.
 */
export default function Contact() {
  return (
    <div role="region" aria-label="Contact">
      <h2 className="text-2xl font-bold text-text-primary">Contact</h2>
      <p className="mt-2 text-sm text-text-secondary">
        Feel free to reach out. I am always open to discussing new opportunities and ideas.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {CONTACT_LINKS.map((link) => {
          const IconComponent = ICON_MAP[link.icon];
          const isClickable = !!link.href;

          const cardClasses =
            'flex items-center gap-4 rounded-lg border border-border bg-bg-card p-4 transition-all duration-250 hover:border-accent hover:bg-bg-card-hover hover:shadow-[0_0_16px_rgba(59,130,246,0.2)] hover:-translate-y-1';

          const content = (
            <>
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded border border-border bg-bg-primary">
                {IconComponent && (
                  <IconComponent size={18} className="text-text-secondary" />
                )}
              </div>
              <div className="min-w-0">
                <p className="text-xs font-mono uppercase tracking-wider text-text-secondary">
                  {link.label}
                </p>
                <p className="mt-0.5 truncate text-sm font-medium text-text-primary">
                  {link.value}
                </p>
              </div>
            </>
          );

          if (isClickable) {
            return (
              <a
                key={link.label}
                href={link.href}
                target={link.href.startsWith('mailto:') ? undefined : '_blank'}
                rel="noopener noreferrer"
                className={`${cardClasses} no-underline`}
                aria-label={`${link.label}: ${link.value}`}
              >
                {content}
              </a>
            );
          }

          return (
            <div
              key={link.label}
              className={cardClasses}
              aria-label={`${link.label}: ${link.value}`}
            >
              {content}
            </div>
          );
        })}
      </div>
    </div>
  );
}
