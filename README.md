# Semantic Anchors for LLMs

[![Deploy to GitHub Pages](https://github.com/LLM-Coding/Semantic-Anchors/actions/workflows/deploy.yml/badge.svg)](https://github.com/LLM-Coding/Semantic-Anchors/actions/workflows/deploy.yml)
[![License](https://img.shields.io/github/license/LLM-Coding/Semantic-Anchors)](LICENSE)
[![Stars](https://img.shields.io/github/stars/LLM-Coding/Semantic-Anchors)](https://github.com/LLM-Coding/Semantic-Anchors/stargazers)

> A curated catalog of well-defined terms, methodologies, and frameworks that serve as reference points when communicating with Large Language Models (LLMs).

## 🌐 Interactive Website

**[Visit the Semantic Anchors website →](https://llm-coding.github.io/Semantic-Anchors/)**

Features:
- 📊 **Interactive Treemap Visualization** - Explore 46+ semantic anchors
- 🎯 **Role-Based Filtering** - Filter by 12 professional roles
- 🔍 **Real-Time Search** - Find anchors by name, tags, or proponents
- 🌙 **Dark/Light Theme** - Comfortable viewing in any environment
- 🌍 **Bilingual UI** - English/German interface (content in English)

## 📖 What are Semantic Anchors?

Semantic anchors are **well-defined terms, methodologies, or frameworks** that act as shared vocabulary between humans and LLMs. They trigger specific, contextually rich knowledge domains within an LLM's training data.

### Examples

- **"TDD, London School"** → Activates: outside-in testing, mock-heavy approach, interaction-based verification
- **"Clean Architecture"** → Activates: Uncle Bob's layered design, dependency rule, use cases as center
- **"SOLID Principles"** → Activates: S.O.L.I.D. breakdown, object-oriented design patterns

### Why Use Them?

- **Precision** - Reduce ambiguity by referencing established knowledge
- **Efficiency** - Activate complex frameworks with minimal tokens
- **Consistency** - Ensure LLMs interpret concepts as the community intends
- **Context Compression** - Convey rich context concisely

## 📚 Content Structure

The catalog is organized as:

```
docs/
├── anchors/          # 46+ individual anchor files
│   ├── tdd-london-school.adoc
│   ├── clean-architecture.adoc
│   └── ...
├── categories/       # 11 MECE-compliant categories
├── roles/            # 12 professional roles
└── metadata/         # Generated metadata for website
```

## 🎯 Browse by Role

Find anchors relevant to your profession:

- [Software Developer / Engineer](docs/roles/software-developer.adoc)
- [Software Architect](docs/roles/software-architect.adoc)
- [QA Engineer / Tester](docs/roles/qa-engineer.adoc)
- [DevOps Engineer](docs/roles/devops-engineer.adoc)
- [Product Owner / Manager](docs/roles/product-owner.adoc)
- [Business Analyst / Requirements Engineer](docs/roles/business-analyst.adoc)
- [Technical Writer / Documentation Specialist](docs/roles/technical-writer.adoc)
- [UX Designer / Researcher](docs/roles/ux-designer.adoc)
- [Data Scientist / Statistician](docs/roles/data-scientist.adoc)
- [Consultant / Coach](docs/roles/consultant.adoc)
- [Team Lead / Engineering Manager](docs/roles/team-lead.adoc)
- [Educator / Trainer](docs/roles/educator.adoc)

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for:

- How to propose new semantic anchors
- Quality criteria for anchors
- Testing methodology with LLMs
- Development setup

### Quick Start

1. **Test your anchor** with an LLM:
   ```
   What concepts do you associate with '<anchor name>'?
   ```
2. **Verify quality criteria**: Precise, Rich, Consistent, Attributable
3. **Create an issue** using our [Propose New Anchor template](https://github.com/LLM-Coding/Semantic-Anchors/issues/new/choose)

## 🛠️ Development

### Prerequisites

- Node.js 20+
- npm

### Setup

```bash
# Clone repository
git clone https://github.com/LLM-Coding/Semantic-Anchors.git
cd Semantic-Anchors

# Install website dependencies
cd website
npm install

# Run development server
npm run dev
# → http://localhost:5173/

# Run tests
npm run test

# Build for production
npm run build
```

### Project Scripts

```bash
# Extract metadata from anchor files
cd scripts
npm install
node extract-metadata.js

# Validate anchors
npm run validate

# Build website
cd website
npm run build
```

## 📋 Documentation

- **[Product Requirements (PRD)](docs/PRD.md)** - Project vision and user stories
- **[Architecture (arc42)](docs/arc42/arc42.adoc)** - Complete technical architecture
- **[Specifications](docs/specs/)** - Use cases, API spec, acceptance criteria
- **[ADRs](docs/specs/adrs/)** - Architecture Decision Records with Pugh matrices
- **[Project Status](PROJECT_STATUS.md)** - Current implementation status

## 🏗️ Architecture

Built with:

- **Vite** - Fast, modern build tool
- **Apache ECharts** - Interactive treemap visualization
- **Tailwind CSS** - Utility-first styling
- **AsciiDoc** - Content format with metadata attributes
- **GitHub Pages** - Hosting and deployment

See [ADRs](docs/specs/adrs/) for detailed decision rationale with Pugh matrix analysis.

## 📊 Project Status

### ✅ Phase 1: Foundation (Complete)
- MECE analysis of categories
- Role mapping for all anchors
- Split README into individual files
- Metadata extraction scripts

### ✅ Phase 2: Website (Complete)
- Interactive treemap visualization
- Role-based filtering
- Real-time search
- i18n (EN/DE)
- Dark/Light theme
- 60 passing tests

### 🚧 Phase 3: Deployment (In Progress)
- GitHub Actions workflow
- Issue templates
- Contributing guide
- Documentation updates

### 🔮 Phase 4: Enhancement (Planned)
- GitHub Copilot validation workflow
- Advanced search features
- Anchor detail view
- Category visualization improvements

## 📈 Statistics

- **46** Semantic Anchors
- **12** Professional Roles
- **11** MECE-compliant Categories
- **60** Passing Tests
- **2** Languages (EN/DE UI)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Architecture & Design**: Claude Sonnet 4.5 (AI-assisted)
- **Maintainer**: [@rdmueller](https://github.com/rdmueller)
- **Community**: All contributors proposing and improving semantic anchors

## 🔗 Links

- **Website**: [https://llm-coding.github.io/Semantic-Anchors/](https://llm-coding.github.io/Semantic-Anchors/)
- **Issues**: [https://github.com/LLM-Coding/Semantic-Anchors/issues](https://github.com/LLM-Coding/Semantic-Anchors/issues)
- **Discussions**: [https://github.com/LLM-Coding/Semantic-Anchors/discussions](https://github.com/LLM-Coding/Semantic-Anchors/discussions)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=LLM-Coding/Semantic-Anchors&type=Date)](https://star-history.com/#LLM-Coding/Semantic-Anchors&Date)
