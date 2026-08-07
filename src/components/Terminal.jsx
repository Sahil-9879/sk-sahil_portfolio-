import { useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import { useTerminal } from '../hooks/useTerminal';
import { PERSONAL } from '../constants/data';

/**
 * Terminal — Linux-style modal terminal.
 * Monospace font, green prompt, dark bg. Escape or click-outside to close.
 * Commands navigate sections or open external links.
 */
export default function Terminal({ isOpen, onClose, onNavigate }) {
  const {
    history,
    input,
    setInput,
    handleKeyDown,
    inputRef,
    scrollRef,
    focusInput,
  } = useTerminal((section) => {
    onNavigate(section);
    onClose();
  });

  // Close on Escape
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      // Small delay to ensure modal is rendered
      const timer = setTimeout(focusInput, 100);
      return () => clearTimeout(timer);
    }
  }, [isOpen, focusInput]);

  // Prevent body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Terminal Window */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="fixed inset-4 z-[101] m-auto flex max-h-[500px] max-w-2xl flex-col overflow-hidden rounded-lg border border-border bg-[#0a0e17] shadow-2xl md:inset-auto md:left-1/2 md:top-1/2 md:-translate-x-1/2 md:-translate-y-1/2 md:w-full"
            role="dialog"
            aria-modal="true"
            aria-label="Terminal"
          >
            {/* Title bar */}
            <div className="flex items-center justify-between border-b border-border px-4 py-2.5">
              <div className="flex items-center gap-2">
                <div className="flex gap-1.5">
                  <button
                    onClick={onClose}
                    className="h-3 w-3 rounded-full bg-red-500/80 hover:bg-red-500 transition-colors cursor-pointer border-none"
                    aria-label="Close terminal"
                  />
                  <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
                  <div className="h-3 w-3 rounded-full bg-green-500/80" />
                </div>
                <span className="ml-3 text-xs font-mono text-text-secondary">
                  visitor@{PERSONAL.name.toLowerCase()}:~
                </span>
              </div>
              <button
                onClick={onClose}
                className="text-text-secondary hover:text-text-primary transition-colors bg-transparent border-none cursor-pointer"
                aria-label="Close terminal"
              >
                <X size={14} />
              </button>
            </div>

            {/* Terminal output */}
            <div
              ref={scrollRef}
              className="flex-1 overflow-y-auto px-4 py-3 font-mono text-sm"
              onClick={focusInput}
            >
              {history.map((entry, i) => (
                <div key={i} className="mb-1">
                  {entry.type === 'input' ? (
                    <div>
                      <span className="text-green-400">
                        visitor@{PERSONAL.name.toLowerCase()}:~$
                      </span>{' '}
                      <span className="text-text-primary">{entry.content}</span>
                    </div>
                  ) : entry.type === 'error' ? (
                    <div className="text-red-400 whitespace-pre-wrap">
                      {entry.content}
                    </div>
                  ) : (
                    <div className="text-text-secondary whitespace-pre-wrap">
                      {entry.content}
                    </div>
                  )}
                </div>
              ))}

              {/* Current input line */}
              <div className="flex items-center">
                <span className="text-green-400 shrink-0">
                  visitor@{PERSONAL.name.toLowerCase()}:~$
                </span>
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="ml-2 flex-1 bg-transparent font-mono text-sm text-text-primary outline-none border-none caret-green-400"
                  autoComplete="off"
                  spellCheck="false"
                  aria-label="Terminal input"
                />
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
