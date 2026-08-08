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
        self.drawString(54, 750, "SK SAHIL — DEVELOPER PORTFOLIO TECHNICAL GUIDE")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(612 - 54, 750, "SYSTEM ARCHITECTURE & BUILD TUTORIAL")
        
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)

        # Bottom Footer
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.75)
        self.line(54, 50, 612 - 54, 50)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 38, "Sk Sahil Portfolio | Technical Overview & Build Tutorial")
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
        alignment=0,
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
        fontSize=15,
        leading=19,
        textColor=c_accent_dark,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
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

    story = []

    # =========================================================================
    # COVER BLOCK
    # =========================================================================
    cover_data = [
        [
            Paragraph("SK SAHIL — DEVELOPER PORTFOLIO", ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10, textColor=c_accent, spaceAfter=6)),
        ],
        [
            Paragraph("Project Architecture, Technical Documentation & Step-by-Step Build Tutorial", title_style),
        ],
        [
            Paragraph("A complete technical guide explaining system design, component architecture, modern technology choices, and step-by-step implementation.", subtitle_style),
        ],
        [
            Paragraph("<b>Author:</b> Sk Sahil | <b>Domain:</b> Computer Science & Cybersecurity<br/><b>Repository:</b> github.com/Sahil-9879 | <b>Live Site:</b> sk-sahil-portfolio.vercel.app", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#cbd5e1"))),
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

    # =========================================================================
    # SECTION 1: PROJECT VISION & ARCHITECTURE OVERVIEW
    # =========================================================================
    story.append(Paragraph("1. Project Vision & Architectural Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))
    story.append(Paragraph(
        "<b>Sk Sahil's Developer Portfolio</b> is an engineer-grade, high-performance web application designed to demonstrate clean code architecture, system performance, and modern frontend practices. "
        "Unlike generic website templates that suffer from bloated JavaScript bundles and slow visual editors, this application was engineered from scratch using <b>React 19, Vite 8, Tailwind CSS v4, Framer Motion, and Linux CLI interaction models</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Key engineering achievements of this project include:",
        body_style
    ))
    
    features_list = [
        "<b>Signature Expanding Horizontal Navigation:</b> A custom flex-grow interpolation layout that dynamically expands the active section tab.",
        "<b>Embedded Interactive Linux Terminal Modal:</b> A functional command-line interface featuring input parsing, history navigation (Up/Down arrows), and section shortcuts.",
        "<b>Single-Source-of-Truth Data Layer:</b> Complete decoupling of content from UI components using a centralized `data.js` structure.",
        "<b>Direct Download Integration:</b> Built-in HTML5 download handlers for instantaneous PDF resume retrieval.",
        "<b>Zero-Bloat Performance:</b> Ultra-lightweight ~110KB compressed bundle size with sub-second page loads."
    ]
    for feat in features_list:
        story.append(Paragraph(f"• {feat}", body_style))

    story.append(Spacer(1, 12))

    # Architecture Comparison Table
    pitch_table_data = [
        [Paragraph("<b>Technical Aspect</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Generic Template Approach</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Sk Sahil's Portfolio Architecture</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Bundle & Speed</b>", body_style),
         Paragraph("3MB+ script footprint, heavy DOM trees", body_style),
         Paragraph("<b>~110KB compressed JS</b>, instant Vite compilation", body_style)],
        
        [Paragraph("<b>UI Components</b>", body_style),
         Paragraph("Tightly-coupled monolithic HTML", body_style),
         Paragraph("<b>Modular React components</b> with clean props", body_style)],
        
        [Paragraph("<b>Interactivity</b>", body_style),
         Paragraph("Basic visual triggers & auto-scroll", body_style),
         Paragraph("<b>Interactive Linux modal terminal</b> CLI emulator", body_style)],
        
        [Paragraph("<b>State & Content</b>", body_style),
         Paragraph("Hardcoded text throughout JSX markup", body_style),
         Paragraph("<b>Decoupled data store</b> (`data.js`)", body_style)],
        
        [Paragraph("<b>Aesthetic & Styling</b>", body_style),
         Paragraph("Bright agency gradients & visual noise", body_style),
         Paragraph("<b>Minimal slate dark mode</b> inspired by developer tools", body_style)]
    ]

    t_pitch = Table(pitch_table_data, colWidths=[110, 185, 209])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pitch)

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: TECHNOLOGIES USED & TOOL BREAKDOWN
    # =========================================================================
    story.append(Paragraph("2. Technology Stack & Tool Mechanics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    tool_data = [
        [
            Paragraph("<b>Technology</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>Tool Functionality & Description</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>Implementation in this Project</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))
        ],
        [
            Paragraph("<b>React 19</b>", body_style),
            Paragraph("Industry-standard JavaScript library for building component-based user interfaces.", body_style),
            Paragraph("Serves as the UI foundation (`Navbar`, `ExpandingNav`, `Terminal`, `Profile`, `Projects`). React state (`useState`, `useCallback`) manages active tabs.", body_style)
        ],
        [
            Paragraph("<b>Vite 8</b>", body_style),
            Paragraph("Next-generation frontend build engine utilizing native ES modules for ultra-fast compilation.", body_style),
            Paragraph("Provides sub-600ms Hot Module Replacement (HMR) during development and builds optimized production bundles.", body_style)
        ],
        [
            Paragraph("<b>Tailwind CSS v4</b>", body_style),
            Paragraph("Utility-first styling framework compiled directly into lightweight CSS.", body_style),
            Paragraph("Configured with custom `@theme` tokens in `src/index.css` defining the Midnight Slate palette, monospace fonts, and hover glow effects.", body_style)
        ],
        [
            Paragraph("<b>Framer Motion</b>", body_style),
            Paragraph("Production motion framework for fluid React layout transitions.", body_style),
            Paragraph("Powers hardware-accelerated entrance and exit animations for the Linux Terminal modal window (`AnimatePresence`).", body_style)
        ],
        [
            Paragraph("<b>Lucide React & Custom SVGs</b>", body_style),
            Paragraph("Scalable vector icon collection matching modern software standards.", body_style),
            Paragraph("Provides UI icons (Mail, FileText, MapPin) along with custom SVG components for GitHub, LinkedIn, LeetCode, and Vercel in `BrandIcons.jsx`.", body_style)
        ],
        [
            Paragraph("<b>Git & GitHub</b>", body_style),
            Paragraph("Distributed version control system and remote repository cloud hosting.", body_style),
            Paragraph("Manages version history at `Sahil-9879/sk_sahil_portfolio` with structured commit milestones.", body_style)
        ],
        [
            Paragraph("<b>Vercel Edge Platform</b>", body_style),
            Paragraph("Global edge cloud network optimized for static single-page application hosting.", body_style),
            Paragraph("Automates continuous deployment on every git push to `main` at `sk-sahil-portfolio.vercel.app`.", body_style)
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
    # SECTION 3: FILE STRUCTURE & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. Directory Layout & Modular Structure", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    tree_text = (
        "sk-sahil-portfolio/\n"
        "├── public/\n"
        "│   ├── resume.pdf                            # Direct PDF download file\n"
        "│   └── Sk_Sahil_Portfolio_Engineering_Guide.pdf  # Technical documentation PDF\n"
        "├── src/\n"
        "│   ├── components/\n"
        "│   │   ├── icons/\n"
        "│   │   │   └── BrandIcons.jsx                # SVG Brand icons (GitHub, LinkedIn, LeetCode, Vercel)\n"
        "│   │   ├── layout/\n"
        "│   │   │   └── Navbar.jsx                    # Header bar with navigation & profile actions\n"
        "│   │   ├── sections/\n"
        "│   │   │   ├── Profile.jsx                   # Hero section & introductory summary\n"
        "│   │   │   ├── About.jsx                     # Background narrative & education timeline\n"
        "│   │   │   ├── Projects.jsx                  # Project cards with GitHub, Vercel & Guide links\n"
        "│   │   │   ├── TechStack.jsx                 # Categorized skills matrix\n"
        "│   │   │   └── Contact.jsx                   # Contact links grid with hover glow effects\n"
        "│   │   ├── ExpandingNav.jsx                  # Signature flex-grow horizontal tab navigation\n"
        "│   │   ├── ContentPanel.jsx                  # Dynamic view container\n"
        "│   │   └── Terminal.jsx                      # Linux-style interactive CLI modal window\n"
        "│   ├── constants/\n"
        "│   │   └── data.js                           # Centralized data store (Single Source of Truth)\n"
        "│   ├── hooks/\n"
        "│   │   └── useTerminal.js                    # Custom React hook for CLI state management\n"
        "│   ├── App.jsx                               # Root layout container\n"
        "│   ├── index.css                             # Tailwind v4 @theme design tokens\n"
        "│   └── main.jsx                              # React 19 DOM mounting entry\n"
        "├── index.html                                # Page head, fonts & SEO metadata\n"
        "└── vite.config.js                            # Vite configuration & plugin pipeline"
    )
    story.append(Paragraph(tree_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: STEP-BY-STEP IMPLEMENTATION TUTORIAL
    # =========================================================================
    story.append(Paragraph("4. Step-by-Step Implementation Tutorial", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Step 1: Project Scaffolding & Setup</b>", h2_style))
    story.append(Paragraph("Scaffold a new Vite React application and install styling and motion libraries:", body_style))
    story.append(Paragraph(
        "npx -y create-vite@latest ./ --template react<br/>"
        "npm install tailwindcss @tailwindcss/vite framer-motion lucide-react",
        code_style
    ))

    story.append(Paragraph("<b>Step 2: Designing Theme Tokens (`src/index.css`)</b>", h2_style))
    story.append(Paragraph("Define dark slate themes and monospace fonts in Tailwind CSS v4:", body_style))
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

    story.append(Paragraph("<b>Step 3: Centralizing Content (`src/constants/data.js`)</b>", h2_style))
    story.append(Paragraph("Store all personal bio details, project metadata, skills, and links in a single file:", body_style))
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

    story.append(Paragraph("<b>Step 4: Building Custom Hooks (`src/hooks/useTerminal.js`)</b>", h2_style))
    story.append(Paragraph("Implement command history, input event keydown listeners, and actions:", body_style))
    story.append(Paragraph(
        "if (trimmed === 'resume') {<br/>"
        "&nbsp;&nbsp;const a = document.createElement('a');<br/>"
        "&nbsp;&nbsp;a.href = PERSONAL.resume;<br/>"
        "&nbsp;&nbsp;a.download = 'Sk_Sahil_Resume.pdf';<br/>"
        "&nbsp;&nbsp;a.click();<br/>"
        "}",
        code_style
    ))

    story.append(Paragraph("<b>Step 5: Git Version Control & Deployment</b>", h2_style))
    story.append(Paragraph(
        "git init<br/>"
        "git add -A<br/>"
        "git commit -m \"feat: Sk Sahil developer portfolio\"<br/>"
        "git remote add origin https://github.com/Sahil-9879/sk_sahil_portfolio.git<br/>"
        "git branch -M main<br/>"
        "git push -u origin main",
        code_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Clean PDF generated: {filename}")

if __name__ == "__main__":
    out_dir = "/home/kalu/.gemini/antigravity/scratch/public"
    downloads_dir = "/home/kalu/Downloads"
    
    os.makedirs(out_dir, exist_ok=True)
    
    pdf_path_public = os.path.join(out_dir, "Sk_Sahil_Portfolio_Engineering_Guide.pdf")
    pdf_path_downloads = os.path.join(downloads_dir, "Sk_Sahil_Portfolio_Engineering_Guide.pdf")
    
    build_pdf(pdf_path_public)
    
    import shutil
    shutil.copy(pdf_path_public, pdf_path_downloads)
    print(f"Copied clean PDF to: {pdf_path_downloads}")
