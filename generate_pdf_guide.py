import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on cover page
        if self._pageNumber == 1:
            self.restoreState()
            return

        # Top Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#3b82f6"))
        self.drawString(54, 750, "SK SAHIL — DEVELOPER PORTFOLIO ENGINEERING GUIDE")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(612 - 54, 750, "TECHNICAL DOCUMENTATION & HR TUTORIAL")
        
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)

        # Bottom Footer
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.75)
        self.line(54, 50, 612 - 54, 50)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 38, "Confidential & Authoritative Documentation | Sk Sahil © 2026")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 38, page_text)
        
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette (Midnight Engineer Theme)
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#3b82f6")      # Blue 500
    c_accent_dark = colors.HexColor("#1d4ed8") # Blue 700
    c_dark_bg = colors.HexColor("#1e293b")     # Slate 800
    c_text_dark = colors.HexColor("#0f172a")   # Primary text
    c_text_muted = colors.HexColor("#475569")  # Subdued text
    c_code_bg = colors.HexColor("#f1f5f9")     # Light slate code bg
    c_border = colors.HexColor("#cbd5e1")      # Border color

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.white,
        alignment=0, # Left-aligned
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#94a3b8"),
        alignment=0,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_accent_dark,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_text_dark,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_text_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=c_code_bg,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e3a8a"),
        backColor=colors.HexColor("#eff6ff"),
        borderColor=colors.HexColor("#93c5fd"),
        borderWidth=0.75,
        borderPadding=8,
        spaceBefore=8,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # COVER BLOCK
    # =========================================================================
    cover_data = [
        [
            Paragraph("SK SAHIL", ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10, textColor=c_accent, spaceAfter=6)),
        ],
        [
            Paragraph("Engineer Portfolio: Complete Architecture, Technical Guide & HR Pitch", title_style),
        ],
        [
            Paragraph("A comprehensive walkthrough explaining project design, modern tech stack, tool mechanics, step-by-step tutorial, and recruiter presentation strategy.", subtitle_style),
        ],
        [
            Paragraph("<b>Author:</b> Sk Sahil | <b>Domain:</b> Computer Science & Cybersecurity<br/><b>Repository:</b> github.com/Sahil-9879 | <b>Live Site:</b> sk_sahil_portfolio.vercel.app", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#cbd5e1"))),
        ]
    ]

    cover_table = Table(cover_data, colWidths=[504])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('PADDING', (0, 0), (-1, -1), 24),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 24),
    ]))
    
    story.append(cover_table)
    story.append(Spacer(1, 14))

    # Executive Overview
    story.append(Paragraph("Executive Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))
    story.append(Paragraph(
        "This official documentation provides an in-depth, production-level breakdown of <b>Sk Sahil's Developer Portfolio</b>. "
        "Unlike standard drag-and-drop website builders or bloated theme templates (such as WordPress, Framer, or Elementor), "
        "this portfolio was architected from first principles using industry-standard engineering tools: <b>React 19, Vite, Tailwind CSS v4, Framer Motion, and Linux CLI concepts</b>.",
        body_style
    ))
    story.append(Paragraph(
        "It serves a dual purpose: first, as a <b>reusable technical tutorial</b> detailing how to construct a high-performance web application from scratch; "
        "and second, as a <b>recruiter-facing pitch guide</b> enabling candidate Sk Sahil to articulate technical decisions, system tradeoffs, and software architecture during HR and technical interviews.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 1: HOW TO EXPLAIN THIS PROJECT TO HR & RECRUITERS
    # =========================================================================
    story.append(Paragraph("1. Explaining the Project to HR & Recruiters", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("1.1 The 60-Second Interview Elevator Pitch", h2_style))
    story.append(Paragraph(
        "<i>\"When an HR manager asks: 'Can you tell me about a project you built recently?'\"</i>",
        callout_style
    ))
    story.append(Paragraph(
        "<b>Suggested Answer:</b><br/>"
        "\"I designed and built my portfolio from scratch as a high-performance single-page web application using <b>React, Vite, and Tailwind CSS v4</b>. "
        "Instead of using generic templates, I engineered it with a <b>developer-focused UI</b> inspired by tools like VS Code and Linux terminals. "
        "Key engineering highlights include a custom-interpolated expanding horizontal navigation bar, an embedded interactive Linux modal terminal with command parsing, "
        "and a single-source-of-truth data structure. I also configured direct PDF resume downloads, responsive design, and automated continuous deployment to <b>Vercel</b> via GitHub CI/CD pipelines.\"",
        body_style
    ))

    story.append(Paragraph("1.2 Why Build an 'Engineer-Grade' Application?", h2_style))
    story.append(Paragraph("Most student portfolios use bright, colorful agency themes or heavy Framer templates that suffer from bloated JavaScript bundles, slow load times, and poor maintainability. Here is how to contrast your work:", body_style))
    
    pitch_table_data = [
        [Paragraph("<b>Dimension</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Generic Template (Framer/WP)</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Sk Sahil's Portfolio (Custom Engineered)</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Performance</b>", body_style),
         Paragraph("Slow (3MB+ bundle size, heavy DOM scripts)", body_style),
         Paragraph("<b>Sub-second load</b> (~110KB gzip bundle, Vite optimized)", body_style)],
        
        [Paragraph("<b>Architecture</b>", body_style),
         Paragraph("Hardcoded HTML or visual editor nodes", body_style),
         Paragraph("<b>Modular React components</b> + strict separation of concerns", body_style)],
        
        [Paragraph("<b>Interactivity</b>", body_style),
         Paragraph("Basic hover effects or scroll triggers", body_style),
         Paragraph("<b>Interactive Linux CLI terminal</b> modal with full command history", body_style)],
        
        [Paragraph("<b>Maintainability</b>", body_style),
         Paragraph("Changes require visual builder tools", body_style),
         Paragraph("<b>Centralized data file</b> (`data.js`); edits take seconds", body_style)],
        
        [Paragraph("<b>Design Tone</b>", body_style),
         Paragraph("Flashy agency gradients & floating blobs", body_style),
         Paragraph("<b>Minimal slate dark mode</b> inspired by developer tools", body_style)]
    ]

    t_pitch = Table(pitch_table_data, colWidths=[100, 190, 214])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pitch)

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: TOOLS USED — WHAT ARE THEY, WHY USED & HOW TO USE THEM
    # =========================================================================
    story.append(Paragraph("2. Tools & Technologies Used (Detailed Breakdown)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("When HR asks <i>'What tools did you use and why?'</i>, use this detailed reference:", body_style))

    tool_data = [
        [
            Paragraph("<b>Tool & Name</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>What Is That Tool?</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>Why Was It Chosen & How Is It Used Here?</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))
        ],
        [
            Paragraph("<b>React 19</b><br/>(Core UI Library)", body_style),
            Paragraph("An open-source JavaScript library developed by Meta for building user interfaces based on components.", body_style),
            Paragraph("Used as the foundation of the app. Enables splitting the website into reusable components (`Navbar`, `ExpandingNav`, `Terminal`, `Contact`). State hooks (`useState`, `useCallback`) manage active tabs and terminal state.", body_style)
        ],
        [
            Paragraph("<b>Vite 8</b><br/>(Build Tool)", body_style),
            Paragraph("A modern, ultra-fast frontend build tool that uses native ES modules to serve code instantly during development.", body_style),
            Paragraph("Replaced legacy Webpack. Provides Instant Hot Module Replacement (HMR) under 600ms and outputs highly compressed bundle chunks (`dist/`) for production.", body_style)
        ],
        [
            Paragraph("<b>Tailwind CSS v4</b><br/>(Styling Engine)", body_style),
            Paragraph("A utility-first CSS framework that compiles utility classes directly into lightweight CSS stylesheet.", body_style),
            Paragraph("Configured with custom `@theme` variables in `src/index.css` to define the Midnight Slate color palette, custom fonts (Inter & JetBrains Mono), and glow effects without external design libraries.", body_style)
        ],
        [
            Paragraph("<b>Framer Motion</b><br/>(Animation)", body_style),
            Paragraph("A production-grade motion library for React that simplifies complex UI animations and layout transitions.", body_style),
            Paragraph("Powers smooth modal entrance/exit transitions for the Linux Terminal modal (`AnimatePresence`, `motion.div`) with hardware-accelerated 60fps performance.", body_style)
        ],
        [
            Paragraph("<b>Lucide React & Custom SVGs</b>", body_style),
            Paragraph("Lightweight SVG icon collection tailored for clean UI interfaces.", body_style),
            Paragraph("Provides standard icons (Mail, FileText, MapPin, Terminal). Custom brand SVGs were engineered for GitHub, LinkedIn, LeetCode, and Vercel in `BrandIcons.jsx`.", body_style)
        ],
        [
            Paragraph("<b>Git & GitHub</b><br/>(Version Control)", body_style),
            Paragraph("Git tracks code revisions locally; GitHub hosts the remote repository on the cloud.", body_style),
            Paragraph("Stores code under `Sahil-9879/sk_sahil_portfolio`. Keeps clean commit history (`git commit`, `git push`) tracking every milestone.", body_style)
        ],
        [
            Paragraph("<b>Vercel Cloud</b><br/>(Hosting & CI/CD)", body_style),
            Paragraph("A global cloud platform optimized for static frontend frameworks with global CDN distribution.", body_style),
            Paragraph("Connected to GitHub repository. Automatically rebuilds and deploys the site every time code is pushed to the `main` branch.", body_style)
        ]
    ]

    t_tools = Table(tool_data, colWidths=[100, 190, 214])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tools)

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 3: SYSTEM ARCHITECTURE & FILE STRUCTURE
    # =========================================================================
    story.append(Paragraph("3. System Architecture & Folder Layout", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("The codebase enforces strict <b>Separation of Concerns (SoC)</b>:", body_style))
    
    tree_text = (
        "sk-sahil-portfolio/\n"
        "├── public/\n"
        "│   └── resume.pdf                 # Direct PDF download file\n"
        "├── src/\n"
        "│   ├── assets/                     # Static media assets\n"
        "│   ├── components/\n"
        "│   │   ├── icons/\n"
        "│   │   │   └── BrandIcons.jsx      # SVG components (GitHub, LinkedIn, LeetCode, Vercel)\n"
        "│   │   ├── layout/\n"
        "│   │   │   └── Navbar.jsx          # Sticky navigation bar with logo & quick links\n"
        "│   │   ├── sections/\n"
        "│   │   │   ├── Profile.jsx         # Hero section & bio summary\n"
        "│   │   │   ├── About.jsx           # Detailed background & education timeline\n"
        "│   │   │   ├── Projects.jsx        # Project cards grid with live & source links\n"
        "│   │   │   ├── TechStack.jsx       # Categorized skills grid\n"
        "│   │   │   └── Contact.jsx         # Contact cards with hover glow effects\n"
        "│   │   ├── ExpandingNav.jsx        # Signature expanding flex navigation\n"
        "│   │   ├── ContentPanel.jsx        # Dynamic tab switcher container\n"
        "│   │   └── Terminal.jsx            # Linux-style modal terminal window\n"
        "│   ├── constants/\n"
        "│   │   └── data.js                 # SINGLE SOURCE OF TRUTH (All content stored here)\n"
        "│   ├── hooks/\n"
        "│   │   └── useTerminal.js          # Custom React hook managing terminal CLI state\n"
        "│   ├── App.jsx                     # Root application container wiring all components\n"
        "│   ├── index.css                   # Tailwind CSS v4 @theme design tokens\n"
        "│   └── main.jsx                    # React 19 entry point mounting to DOM\n"
        "├── index.html                      # HTML5 page head with Google Fonts & SEO meta tags\n"
        "├── package.json                    # Dependencies & build scripts\n"
        "└── vite.config.js                  # Vite configuration & Tailwind plugin wiring"
    )
    story.append(Paragraph(tree_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: STEP-BY-STEP BUILD TUTORIAL
    # =========================================================================
    story.append(Paragraph("4. Step-by-Step Build Tutorial", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Step 1: Scaffold Project with Vite & Install Dependencies</b>", h2_style))
    story.append(Paragraph("Run the following terminal commands to create an empty Vite React project and install styling/animation packages:", body_style))
    story.append(Paragraph(
        "# Create Vite project in current directory<br/>"
        "npx -y create-vite@latest ./ --template react<br/><br/>"
        "# Install core dependencies<br/>"
        "npm install tailwindcss @tailwindcss/vite framer-motion lucide-react",
        code_style
    ))

    story.append(Paragraph("<b>Step 2: Configure Tailwind v4 Theme Tokens (`src/index.css`)</b>", h2_style))
    story.append(Paragraph("Tailwind v4 uses CSS `@theme` blocks rather than JS configuration files. Define midnight colors and custom font families:", body_style))
    story.append(Paragraph(
        "@import \"tailwindcss\";<br/><br/>"
        "@theme {<br/>"
        "&nbsp;&nbsp;--color-bg-primary: #0a0e17;<br/>"
        "&nbsp;&nbsp;--color-bg-card: #111827;<br/>"
        "&nbsp;&nbsp;--color-bg-card-hover: #1f2937;<br/>"
        "&nbsp;&nbsp;--color-text-primary: #f3f4f6;<br/>"
        "&nbsp;&nbsp;--color-text-secondary: #9ca3af;<br/>"
        "&nbsp;&nbsp;--color-accent: #3b82f6;<br/>"
        "&nbsp;&nbsp;--color-border: #1f2937;<br/>"
        "&nbsp;&nbsp;--font-sans: 'Inter', sans-serif;<br/>"
        "&nbsp;&nbsp;--font-mono: 'JetBrains Mono', monospace;<br/>"
        "}",
        code_style
    ))

    story.append(Paragraph("<b>Step 3: Centralize Data Layer (`src/constants/data.js`)</b>", h2_style))
    story.append(Paragraph("Decouple content from UI components so edits never break JSX markup. Example `PERSONAL` and `CONTACT_LINKS` object structure:", body_style))
    story.append(Paragraph(
        "export const PERSONAL = {<br/>"
        "&nbsp;&nbsp;name: 'Sk Sahil',<br/>"
        "&nbsp;&nbsp;role: 'Tech & Cybersecurity Enthusiast',<br/>"
        "&nbsp;&nbsp;college: 'B.Tech Computer Science',<br/>"
        "&nbsp;&nbsp;email: 'sksahil01018@gmail.com',<br/>"
        "&nbsp;&nbsp;github: 'https://github.com/Sahil-9879',<br/>"
        "&nbsp;&nbsp;linkedin: 'https://www.linkedin.com/in/sk-sahil-061a5a373/',<br/>"
        "&nbsp;&nbsp;leetcode: 'https://leetcode.com/u/sahil_0205/',<br/>"
        "&nbsp;&nbsp;resume: '/resume.pdf',<br/>"
        "};",
        code_style
    ))

    story.append(Paragraph("<b>Step 4: Build Custom React Hooks (`src/hooks/useTerminal.js`)</b>", h2_style))
    story.append(Paragraph("Implement terminal command parsing (`help`, `about`, `projects`, `skills`, `contact`, `resume`) and direct file downloads:", body_style))
    story.append(Paragraph(
        "if (trimmed === 'resume') {<br/>"
        "&nbsp;&nbsp;const a = document.createElement('a');<br/>"
        "&nbsp;&nbsp;a.href = PERSONAL.resume;<br/>"
        "&nbsp;&nbsp;a.download = 'Sk_Sahil_Resume.pdf';<br/>"
        "&nbsp;&nbsp;a.click();<br/>"
        "}",
        code_style
    ))

    story.append(Paragraph("<b>Step 5: Wire Resume Download Links</b>", h2_style))
    story.append(Paragraph("Add the HTML5 `download=\"Sk_Sahil_Resume.pdf\"` attribute to all resume anchor tags across `Navbar.jsx`, `Profile.jsx`, and `Contact.jsx` to ensure seamless, direct downloads when users click.", body_style))

    story.append(Paragraph("<b>Step 6: Version Control & Deploy to Vercel</b>", h2_style))
    story.append(Paragraph(
        "# Initialize Git & commit changes<br/>"
        "git init<br/>"
        "git add -A<br/>"
        "git commit -m \"initial commit: Sk Sahil Portfolio\"<br/><br/>"
        "# Push to GitHub<br/>"
        "git remote add origin https://github.com/Sahil-9879/sk_sahil_portfolio.git<br/>"
        "git branch -M main<br/>"
        "git push -u origin main",
        code_style
    ))
    story.append(Paragraph("Connect the repository on <b>Vercel.com</b>. Vercel automatically runs `npm run build` and serves the app on global edge servers.", body_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 5: INTERVIEW PREPARATION CHEATSHEET
    # =========================================================================
    story.append(Paragraph("5. HR & Technical Interview Q&A Cheatsheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    qa_list = [
        ("Q1: Why did you build this portfolio yourself instead of using template platforms like WordPress or Framer?",
         "<b>Answer:</b> As a Computer Science student specializing in cybersecurity and software engineering, I wanted my personal site to reflect real code craft. Building it with React and Tailwind gave me complete control over performance (sub-second load time), accessibility, responsive layout behavior, and security best practices without third-party tracker bloat."),
        
        ("Q2: What is the most unique feature of your portfolio, and how did you implement it?",
         "<b>Answer:</b> The interactive Linux-style modal terminal. I created a custom React hook (`useTerminal`) that maintains command history, handles keyboard events (like Up/Down arrow navigation and Enter key execution), and parses custom commands to dynamically switch sections or trigger direct resume PDF downloads."),
        
        ("Q3: How do you handle code updates when you want to change your bio, skills, or projects?",
         "<b>Answer:</b> I engineered a single-source-of-truth data pattern (`data.js`). Content is completely separated from rendering code. Updating a project or skill requires editing a single Javascript object without risking JSX layout breakages."),
        
        ("Q4: How did you ensure fast loading speeds and smooth responsiveness?",
         "<b>Answer:</b> I used Vite 8 for fast bundle splitting (~110KB gzipped JS), Tailwind CSS v4 for zero-runtime utility styling, and Framer Motion for hardware-accelerated GPU transitions. The layout uses CSS Grid and Flexbox for fluid responsiveness across mobile, tablet, and desktop viewports."),
        
        ("Q5: How is continuous deployment configured for your portfolio?",
         "<b>Answer:</b> I connected my GitHub repository (`Sahil-9879/sk_sahil_portfolio`) to Vercel's CI/CD pipeline. Every git push to the `main` branch triggers an automated build verification and deploys the live production bundle in seconds.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 4))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    out_dir = "/home/kalu/.gemini/antigravity/scratch/public"
    downloads_dir = "/home/kalu/Downloads"
    
    os.makedirs(out_dir, exist_ok=True)
    
    pdf_path_public = os.path.join(out_dir, "Sk_Sahil_Portfolio_Engineering_Guide.pdf")
    pdf_path_downloads = os.path.join(downloads_dir, "Sk_Sahil_Portfolio_Engineering_Guide.pdf")
    
    build_pdf(pdf_path_public)
    
    # Copy to Downloads directory
    import shutil
    shutil.copy(pdf_path_public, pdf_path_downloads)
    print(f"Copied to: {pdf_path_downloads}")
