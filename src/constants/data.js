/**
 * Portfolio Data — Single source of truth for all content.
 * Update this file with your actual information.
 */

export const PERSONAL = {
  name: 'Kalu',
  role: 'Backend Developer & Cybersecurity Enthusiast',
  college: 'B.Tech Computer Science',
  location: 'India',
  email: 'kalu@example.com',
  github: 'https://github.com/kalu',
  linkedin: 'https://linkedin.com/in/kalu',
  resume: '/resume.pdf',
  avatar: null, // Replace with your image path
  intro:
    'Computer Science student passionate about building robust backend systems and exploring cybersecurity. I write clean, maintainable code and believe in engineering software that scales.',
};

export const ABOUT = {
  bio: [
    'I am a Computer Science undergraduate with a deep interest in backend engineering and cybersecurity. My journey started with writing simple Python scripts and evolved into building distributed systems, securing networks, and contributing to open-source projects.',
    'I focus on writing production-grade code — clean architecture, proper error handling, and comprehensive testing are non-negotiable. I believe the best software is built with discipline, not just talent.',
    'When I am not coding, you will find me reading RFCs, experimenting with CTF challenges, or setting up homelabs to test infrastructure configurations.',
  ],
  education: [
    {
      degree: 'B.Tech in Computer Science & Engineering',
      institution: 'University Name',
      period: '2022 — 2026',
      description:
        'Specializing in backend systems, distributed computing, and information security.',
    },
    {
      degree: 'Higher Secondary (XII)',
      institution: 'School Name',
      period: '2020 — 2022',
      description: 'Science stream with Computer Science. Scored 92%.',
    },
  ],
  interests: [
    'Distributed Systems',
    'Network Security',
    'Operating Systems',
    'Open Source',
    'CTF Competitions',
    'System Design',
  ],
};

export const PROJECTS = [
  {
    name: 'SecureVault',
    description:
      'End-to-end encrypted file storage system with zero-knowledge architecture. Built with AES-256 encryption, secure key derivation, and a RESTful API backend.',
    tech: ['Java', 'Spring Boot', 'PostgreSQL', 'Docker', 'AES-256'],
    github: 'https://github.com/kalu/securevault',
    demo: null,
  },
  {
    name: 'NetSentinel',
    description:
      'Real-time network intrusion detection system that monitors traffic patterns, detects anomalies using ML models, and generates alerts.',
    tech: ['Python', 'Scapy', 'TensorFlow', 'Redis', 'Docker'],
    github: 'https://github.com/kalu/netsentinel',
    demo: null,
  },
  {
    name: 'TaskForge API',
    description:
      'Production-grade task management REST API with JWT authentication, role-based access control, rate limiting, and comprehensive test coverage.',
    tech: ['Node.js', 'Express', 'MongoDB', 'Redis', 'Jest'],
    github: 'https://github.com/kalu/taskforge-api',
    demo: 'https://taskforge-api.example.com',
  },
  {
    name: 'PacketSniffer',
    description:
      'Low-level network packet analyzer built from scratch. Captures, parses, and visualizes TCP/UDP/ICMP packets with filtering capabilities.',
    tech: ['C', 'Linux', 'Sockets', 'ncurses'],
    github: 'https://github.com/kalu/packetsniffer',
    demo: null,
  },
  {
    name: 'AuthShield',
    description:
      'Authentication microservice implementing OAuth 2.0, TOTP-based 2FA, and session management with secure cookie handling.',
    tech: ['Go', 'PostgreSQL', 'Redis', 'gRPC', 'Docker'],
    github: 'https://github.com/kalu/authshield',
    demo: null,
  },
  {
    name: 'LogStream',
    description:
      'Centralized log aggregation pipeline that collects, processes, and indexes logs from distributed services with real-time search.',
    tech: ['Python', 'Kafka', 'Elasticsearch', 'Docker', 'Grafana'],
    github: 'https://github.com/kalu/logstream',
    demo: null,
  },
];

export const SKILLS = {
  Languages: ['Java', 'Python', 'C', 'Go', 'JavaScript', 'SQL', 'Bash'],
  Frameworks: [
    'Spring Boot',
    'Express.js',
    'Flask',
    'React',
    'Tailwind CSS',
  ],
  'Tools & Platforms': [
    'Docker',
    'Git',
    'Linux',
    'Nginx',
    'Jenkins',
    'AWS',
  ],
  'Databases': ['PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch'],
  'Security & Networking': [
    'Wireshark',
    'Burp Suite',
    'Nmap',
    'Metasploit',
    'TCP/IP',
    'REST API',
  ],
  Concepts: [
    'System Design',
    'Microservices',
    'CI/CD',
    'Cryptography',
    'OAuth 2.0',
    'Networking',
  ],
};

export const CONTACT_LINKS = [
  {
    label: 'Email',
    value: 'kalu@example.com',
    href: 'mailto:kalu@example.com',
    icon: 'Mail',
  },
  {
    label: 'GitHub',
    value: 'github.com/kalu',
    href: 'https://github.com/kalu',
    icon: 'Github',
  },
  {
    label: 'LinkedIn',
    value: 'linkedin.com/in/kalu',
    href: 'https://linkedin.com/in/kalu',
    icon: 'Linkedin',
  },
  {
    label: 'Resume',
    value: 'Download PDF',
    href: '/resume.pdf',
    icon: 'FileText',
  },
  {
    label: 'Location',
    value: 'India',
    href: null,
    icon: 'MapPin',
  },
];

export const NAV_SECTIONS = ['About', 'Projects', 'Tech Stack', 'Contact'];

export const TERMINAL_COMMANDS = {
  help: `Available commands:
  about       — Learn about me
  projects    — View my projects
  skills      — See my tech stack
  contact     — Get my contact info
  resume      — Open my resume
  github      — Visit my GitHub
  linkedin    — Visit my LinkedIn
  clear       — Clear terminal
  help        — Show this help message`,
  about: `${PERSONAL.name} — ${PERSONAL.role}

${ABOUT.bio[0]}

Education: ${ABOUT.education[0].degree}
           ${ABOUT.education[0].institution} (${ABOUT.education[0].period})`,
  projects: PROJECTS.map(
    (p, i) => `${i + 1}. ${p.name}\n   ${p.description.slice(0, 80)}...\n   Stack: ${p.tech.join(', ')}`
  ).join('\n\n'),
  skills: Object.entries(SKILLS)
    .map(([cat, items]) => `${cat}: ${items.join(', ')}`)
    .join('\n'),
  contact: CONTACT_LINKS.map((c) => `${c.label}: ${c.value}`).join('\n'),
};
