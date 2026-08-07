/**
 * Portfolio Data — Single source of truth for all content.
 * Update this file with your actual information.
 */

export const PERSONAL = {
  name: 'Sk Sahil',
  role: 'Tech & Cybersecurity Enthusiast',
  college: 'B.Tech Computer Science',
  location: 'India',
  email: 'sksahil01018@gmail.com',
  github: 'https://github.com/Sahil-9879',
  linkedin: 'https://www.linkedin.com/in/sk-sahil-061a5a373/',
  leetcode: 'https://leetcode.com/u/sahil_0205/',
  resume: '/resume.pdf',
  avatar: null, // Replace with your image path
  intro:
    'Computer Science student passionate about exploring cybersecurity and building new projects. I write clean, maintainable code and believe in engineering software that scales.',
};

export const ABOUT = {
  bio: [
    'I am a Computer Science undergraduate with a deep interest in coding and cybersecurity. My journey started with writing simple Python scripts and doing small Java projects and evolved into building different data visualisation dashboards, a small Java bug finder, and a to-do list, and contributing to open-source projects.',
    'I focus on writing production-grade code — clean architecture, proper error handling, and comprehensive testing are non-negotiable. I believe the best software is built with discipline and no-negotiating focus.',
    'When I am not coding, you will find me reading books or most probably getting engaged in some physical work as I believe being fit and enjoying your hobbies make you even more productive in the work that needs to be done.',
  ],
  education: [
    {
      degree: 'B.Tech in Computer Science & Engineering',
      institution: 'University Name',
      period: '2022 — 2026 (Graduating Year: 2028)',
      description:
        'B.Tech in Computer Science (Core). Domain: Cybersecurity.',
    },
    {
      degree: 'X & XII',
      institution: 'Kendriya Vidyalaya NTPC Kaniha',
      period: '2012 — 2024',
      description: 'Science stream with Computer Science.',
    },
  ],
  interests: [
    'Development',
    'Network Security',
    'Operating Systems',
    'Red Teaming',
    'CTF / Hackathons',
    'Competitive Coding',
  ],
};

export const PROJECTS = [
  {
    name: 'Sk Sahil — Developer Portfolio',
    description:
      'Engineer-focused, responsive portfolio application featuring expanding horizontal tab navigation, Linux-style interactive modal terminal, dark theme, and single accent palette.',
    tech: ['React', 'Vite', 'Tailwind CSS', 'Framer Motion'],
    github: 'https://github.com/Sahil-9879',
    demo: 'https://vercel.com',
  },
];

export const SKILLS = {
  Languages: ['Java', 'Python', 'C', 'SQL', 'Bash'],
  Frameworks: [
    'ROS',
    'Streamlit',
    'Panel',
    'Tailwind CSS',
  ],
  'Tools & Platforms': [
    'LeetCode',
    'VS Code',
    'Kaggle',
    'Git',
    'Linux',
    'AWS',
  ],
  'Databases': ['MySQL'],
  'Security & Networking': [
    'Wireshark',
    'Burp Suite',
    'Nmap',
    'Metasploit',
    'TCP/IP',
    'REST API',
  ],
  Concepts: [
    'OOPs',
    'DBMS',
    'OS',
    'System Design',
    'Networking',
  ],
};

export const CONTACT_LINKS = [
  {
    label: 'Email',
    value: 'sksahil01018@gmail.com',
    href: 'mailto:sksahil01018@gmail.com',
    icon: 'Mail',
  },
  {
    label: 'GitHub',
    value: 'github.com/Sahil-9879',
    href: 'https://github.com/Sahil-9879',
    icon: 'Github',
  },
  {
    label: 'LinkedIn',
    value: 'sk-sahil-061a5a373',
    href: 'https://www.linkedin.com/in/sk-sahil-061a5a373/',
    icon: 'Linkedin',
  },
  {
    label: 'LeetCode',
    value: 'sahil_0205',
    href: 'https://leetcode.com/u/sahil_0205/',
    icon: 'LeetCode',
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
