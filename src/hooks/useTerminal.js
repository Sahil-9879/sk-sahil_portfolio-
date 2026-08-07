import { useState, useCallback, useRef, useEffect } from 'react';
import { TERMINAL_COMMANDS, PERSONAL } from '../constants/data';

/**
 * Custom hook for terminal state management.
 * Handles command input, history, output, and navigation actions.
 */
export function useTerminal(onNavigate) {
  const [history, setHistory] = useState([
    {
      type: 'output',
      content: `Welcome to ${PERSONAL.name}'s terminal. Type "help" for available commands.`,
    },
  ]);
  const [input, setInput] = useState('');
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const inputRef = useRef(null);
  const scrollRef = useRef(null);

  // Auto-scroll to bottom on new output
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history]);

  // Focus input when terminal opens
  const focusInput = useCallback(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const executeCommand = useCallback(
    (cmd) => {
      const trimmed = cmd.trim().toLowerCase();
      const newHistory = [
        ...history,
        { type: 'input', content: cmd.trim() },
      ];

      if (trimmed === 'clear') {
        setHistory([]);
        setInput('');
        return;
      }

      if (trimmed === 'resume') {
        newHistory.push({
          type: 'output',
          content: 'Opening resume...',
        });
        setHistory(newHistory);
        window.open(PERSONAL.resume, '_blank');
      } else if (trimmed === 'github') {
        newHistory.push({
          type: 'output',
          content: `Opening ${PERSONAL.github}...`,
        });
        setHistory(newHistory);
        window.open(PERSONAL.github, '_blank');
      } else if (trimmed === 'linkedin') {
        newHistory.push({
          type: 'output',
          content: `Opening ${PERSONAL.linkedin}...`,
        });
        setHistory(newHistory);
        window.open(PERSONAL.linkedin, '_blank');
      } else if (['about', 'projects', 'skills', 'contact'].includes(trimmed)) {
        const sectionMap = {
          about: 'About',
          projects: 'Projects',
          skills: 'Tech Stack',
          contact: 'Contact',
        };
        newHistory.push({
          type: 'output',
          content: TERMINAL_COMMANDS[trimmed] || `Navigating to ${sectionMap[trimmed]}...`,
        });
        setHistory(newHistory);
        if (onNavigate) {
          onNavigate(sectionMap[trimmed]);
        }
      } else if (trimmed === 'help') {
        newHistory.push({
          type: 'output',
          content: TERMINAL_COMMANDS.help,
        });
        setHistory(newHistory);
      } else if (trimmed === '') {
        setHistory(newHistory);
      } else {
        newHistory.push({
          type: 'error',
          content: `Command not found: ${cmd.trim()}. Type "help" for available commands.`,
        });
        setHistory(newHistory);
      }

      setCommandHistory((prev) => [...prev, cmd.trim()]);
      setHistoryIndex(-1);
      setInput('');
    },
    [history, onNavigate]
  );

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === 'Enter') {
        executeCommand(input);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (commandHistory.length > 0) {
          const newIndex =
            historyIndex === -1
              ? commandHistory.length - 1
              : Math.max(0, historyIndex - 1);
          setHistoryIndex(newIndex);
          setInput(commandHistory[newIndex]);
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (historyIndex !== -1) {
          const newIndex = historyIndex + 1;
          if (newIndex >= commandHistory.length) {
            setHistoryIndex(-1);
            setInput('');
          } else {
            setHistoryIndex(newIndex);
            setInput(commandHistory[newIndex]);
          }
        }
      }
    },
    [input, executeCommand, commandHistory, historyIndex]
  );

  return {
    history,
    input,
    setInput,
    handleKeyDown,
    inputRef,
    scrollRef,
    focusInput,
  };
}
