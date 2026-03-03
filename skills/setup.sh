#!/bin/bash
# Setup AI Skills for Dynasif - PowerBuilder 11.5 project
# Configures AI coding assistants that follow agentskills.io standard:
#   - Claude Code: .claude/skills/ symlink
#   - Gemini CLI: .gemini/skills/ symlink
#   - Codex (OpenAI): .codex/skills/ symlink
#   - GitHub Copilot: .github/copilot-instructions.md copy
#
# Usage:
#   ./skills/setup.sh              # Interactive mode (select AI assistants)
#   ./skills/setup.sh --all        # Configure all AI assistants
#   ./skills/setup.sh --claude     # Configure only Claude Code
#   ./skills/setup.sh --claude --gemini  # Configure multiple

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_SOURCE="$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Selection flags
SETUP_CLAUDE=false
SETUP_GEMINI=false
SETUP_CODEX=false
SETUP_COPILOT=false

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Configure AI coding assistants for Dynasif development."
    echo ""
    echo "Options:"
    echo "  --all       Configure all AI assistants"
    echo "  --claude    Configure Claude Code"
    echo "  --gemini    Configure Gemini CLI"
    echo "  --codex     Configure Codex (OpenAI)"
    echo "  --copilot   Configure GitHub Copilot"
    echo "  --help      Show this help message"
    echo ""
    echo "If no options provided, runs in interactive mode."
    echo ""
    echo "Examples:"
    echo "  $0                      # Interactive selection"
    echo "  $0 --all                # All AI assistants"
    echo "  $0 --claude --gemini    # Only Claude and Gemini"
}

show_menu() {
    echo -e "${BOLD}Which AI assistants do you use?${NC}"
    echo -e "${CYAN}(Use numbers to toggle, Enter to confirm)${NC}"
    echo ""

    local options=("Claude Code" "Gemini CLI" "Codex (OpenAI)" "GitHub Copilot")
    local selected=(true false false false)  # Claude selected by default

    while true; do
        for i in "${!options[@]}"; do
            if [ "${selected[$i]}" = true ]; then
                echo -e "  ${GREEN}[x]${NC} $((i+1)). ${options[$i]}"
            else
                echo -e "  [ ] $((i+1)). ${options[$i]}"
            fi
        done
        echo ""
        echo -e "  ${YELLOW}a${NC}. Select all"
        echo -e "  ${YELLOW}n${NC}. Select none"
        echo ""
        echo -n "Toggle (1-4, a, n) or Enter to confirm: "

        read -r choice

        case $choice in
            1) selected[0]=$([ "${selected[0]}" = true ] && echo false || echo true) ;;
            2) selected[1]=$([ "${selected[1]}" = true ] && echo false || echo true) ;;
            3) selected[2]=$([ "${selected[2]}" = true ] && echo false || echo true) ;;
            4) selected[3]=$([ "${selected[3]}" = true ] && echo false || echo true) ;;
            a|A) selected=(true true true true) ;;
            n|N) selected=(false false false false) ;;
            "") break ;;
            *) echo -e "${RED}Invalid option${NC}" ;;
        esac

        # Move cursor up to redraw menu
        echo -en "\033[10A\033[J"
    done

    SETUP_CLAUDE=${selected[0]}
    SETUP_GEMINI=${selected[1]}
    SETUP_CODEX=${selected[2]}
    SETUP_COPILOT=${selected[3]}
}

setup_claude() {
    local target_skills="$REPO_ROOT/.claude/skills"

    if [ ! -d "$REPO_ROOT/.claude" ]; then
        mkdir -p "$REPO_ROOT/.claude"
    fi

    # Skills symlink
    if [ -L "$target_skills" ]; then
        rm "$target_skills"
    elif [ -d "$target_skills" ]; then
        mv "$target_skills" "$REPO_ROOT/.claude/skills.backup.$(date +%s)"
    fi

    ln -s "$SKILLS_SOURCE" "$target_skills"
    echo -e "${GREEN}  ✓ .claude/skills -> skills/${NC}"
    echo -e "${CYAN}    Claude will read CLAUDE.md + skills/${NC}"
}

setup_gemini() {
    local target_skills="$REPO_ROOT/.gemini/skills"

    if [ ! -d "$REPO_ROOT/.gemini" ]; then
        mkdir -p "$REPO_ROOT/.gemini"
    fi

    # Skills symlink
    if [ -L "$target_skills" ]; then
        rm "$target_skills"
    elif [ -d "$target_skills" ]; then
        mv "$target_skills" "$REPO_ROOT/.gemini/skills.backup.$(date +%s)"
    fi

    ln -s "$SKILLS_SOURCE" "$target_skills"
    echo -e "${GREEN}  ✓ .gemini/skills -> skills/${NC}"
    echo -e "${CYAN}    Gemini will read AGENTS.md + skills/${NC}"
}

setup_codex() {
    local target_skills="$REPO_ROOT/.codex/skills"

    if [ ! -d "$REPO_ROOT/.codex" ]; then
        mkdir -p "$REPO_ROOT/.codex"
    fi

    # Skills symlink
    if [ -L "$target_skills" ]; then
        rm "$target_skills"
    elif [ -d "$target_skills" ]; then
        mv "$target_skills" "$REPO_ROOT/.codex/skills.backup.$(date +%s)"
    fi

    ln -s "$SKILLS_SOURCE" "$target_skills"
    echo -e "${GREEN}  ✓ .codex/skills -> skills/${NC}"
    echo -e "${CYAN}    Codex will read AGENTS.md + skills/${NC}"
}

setup_copilot() {
    if [ -f "$REPO_ROOT/AGENTS.md" ]; then
        mkdir -p "$REPO_ROOT/.github"
        cp "$REPO_ROOT/AGENTS.md" "$REPO_ROOT/.github/copilot-instructions.md"
        echo -e "${GREEN}  ✓ AGENTS.md -> .github/copilot-instructions.md${NC}"
        echo -e "${CYAN}    Copilot will read copilot-instructions.md${NC}"
    else
        echo -e "${YELLOW}  ! AGENTS.md not found, skipping Copilot setup${NC}"
    fi
}

# =============================================================================
# PARSE ARGUMENTS
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            SETUP_CLAUDE=true
            SETUP_GEMINI=true
            SETUP_CODEX=true
            SETUP_COPILOT=true
            shift
            ;;
        --claude)
            SETUP_CLAUDE=true
            shift
            ;;
        --gemini)
            SETUP_GEMINI=true
            shift
            ;;
        --codex)
            SETUP_CODEX=true
            shift
            ;;
        --copilot)
            SETUP_COPILOT=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# =============================================================================
# MAIN
# =============================================================================

echo "🤖 Dynasif AI Skills Setup - PowerBuilder 11.5"
echo "==============================================="
echo ""

# Count skills
SKILL_COUNT=$(find "$SKILLS_SOURCE" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$SKILL_COUNT" -eq 0 ]; then
    echo -e "${RED}No skills found in $SKILLS_SOURCE${NC}"
    exit 1
fi

echo -e "${BLUE}Found $SKILL_COUNT PowerBuilder skills to configure:${NC}"
echo "  • datawindow - .srd editing, DDDW, validations"
echo "  • functions  - Syntax, tildes, variable declaration"
echo "  • window     - Events, controls, patterns"
echo "  • nvo        - Clean Architecture, business logic"
echo ""

# Interactive mode if no flags provided
if [ "$SETUP_CLAUDE" = false ] && [ "$SETUP_GEMINI" = false ] && [ "$SETUP_CODEX" = false ] && [ "$SETUP_COPILOT" = false ]; then
    show_menu
    echo ""
fi

# Check if at least one selected
if [ "$SETUP_CLAUDE" = false ] && [ "$SETUP_GEMINI" = false ] && [ "$SETUP_CODEX" = false ] && [ "$SETUP_COPILOT" = false ]; then
    echo -e "${YELLOW}No AI assistants selected. Nothing to do.${NC}"
    exit 0
fi

# Run selected setups
STEP=1
TOTAL=0
[ "$SETUP_CLAUDE" = true ] && TOTAL=$((TOTAL + 1))
[ "$SETUP_GEMINI" = true ] && TOTAL=$((TOTAL + 1))
[ "$SETUP_CODEX" = true ] && TOTAL=$((TOTAL + 1))
[ "$SETUP_COPILOT" = true ] && TOTAL=$((TOTAL + 1))

if [ "$SETUP_CLAUDE" = true ]; then
    echo -e "${YELLOW}[$STEP/$TOTAL] Setting up Claude Code...${NC}"
    setup_claude
    STEP=$((STEP + 1))
fi

if [ "$SETUP_GEMINI" = true ]; then
    echo -e "${YELLOW}[$STEP/$TOTAL] Setting up Gemini CLI...${NC}"
    setup_gemini
    STEP=$((STEP + 1))
fi

if [ "$SETUP_CODEX" = true ]; then
    echo -e "${YELLOW}[$STEP/$TOTAL] Setting up Codex (OpenAI)...${NC}"
    setup_codex
    STEP=$((STEP + 1))
fi

if [ "$SETUP_COPILOT" = true ]; then
    echo -e "${YELLOW}[$STEP/$TOTAL] Setting up GitHub Copilot...${NC}"
    setup_copilot
fi

# =============================================================================
# SUMMARY
# =============================================================================
echo ""
echo -e "${GREEN}✅ Successfully configured $SKILL_COUNT PowerBuilder skills + reglas!${NC}"
echo ""
echo "Configured:"
[ "$SETUP_CLAUDE" = true ] && echo "  • Claude Code:    .claude/skills/ → skills/ + .claude/reglas/ → docs/reglas/"
[ "$SETUP_GEMINI" = true ] && echo "  • Gemini CLI:     .gemini/skills/ → skills/ + .gemini/reglas/ → docs/reglas/"
[ "$SETUP_CODEX" = true ] && echo "  • Codex (OpenAI): .codex/skills/ → skills/ + .codex/reglas/ → docs/reglas/"
[ "$SETUP_COPILOT" = true ] && echo "  • GitHub Copilot: .github/copilot-instructions.md"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Restart your AI assistant to load the skills + reglas"
echo "  2. Skills will auto-invoke based on file types:"
echo "     - .srd files → datawindow skill"
echo "     - .srf files → functions skill"
echo "     - .srw files → window skill"
echo "     - nvo_* objects → nvo skill"
echo "  3. AI assistants can now read docs/reglas/ for:"
echo "     - Git workflow (including QA approval policy)"
echo "     - PowerBuilder syntax rules"
echo "     - DataWindow editing guidelines"
echo "     - Clean Architecture patterns"
echo ""
echo -e "${BLUE}Note: AGENTS.md and CLAUDE.md reference these skills + reglas.${NC}"
