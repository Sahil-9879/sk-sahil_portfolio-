import { AnimatePresence, motion } from 'framer-motion';
import About from './sections/About';
import Projects from './sections/Projects';
import TechStack from './sections/TechStack';
import Contact from './sections/Contact';

const SECTION_MAP = {
  About: About,
  Projects: Projects,
  'Tech Stack': TechStack,
  Contact: Contact,
};

/**
 * ContentPanel — Renders the active section's content.
 * Bordered container with fixed height, dark bg, and overflow scroll.
 * Subtle fade transition between sections.
 */
export default function ContentPanel({ activeSection }) {
  const ActiveComponent = SECTION_MAP[activeSection];

  if (!ActiveComponent) return null;

  return (
    <div
      id={`panel-${activeSection.toLowerCase().replace(/\s+/g, '-')}`}
      role="tabpanel"
      aria-label={`${activeSection} content`}
      className="border border-t-0 border-border rounded-b-lg bg-bg-card overflow-y-auto"
      style={{ height: 'clamp(400px, 55vh, 600px)' }}
    >
      <AnimatePresence mode="wait">
        <motion.div
          key={activeSection}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
          className="p-6 md:p-8"
        >
          <ActiveComponent />
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
