#!/usr/bin/env bash
# Installs the presentation toolkit: Guizang PPT skill, OpenDesign (+ its deck skills),
# Quarkdown and Spectacle. Re-runnable. Needs network access to github.com,
# registry.npmjs.org and nodejs.org (and raw.githubusercontent.com for Quarkdown).
set -euo pipefail

TOOLS_DIR="${TOOLS_DIR:-$HOME/tools}"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$TOOLS_DIR" "$SKILLS_DIR"

clone_or_pull() {  # $1 = owner/repo
  local dir="$TOOLS_DIR/${1#*/}"
  if [ -d "$dir/.git" ]; then git -C "$dir" pull --ff-only -q || true; else git clone -q --depth 1 "https://github.com/$1.git" "$dir"; fi
}

for repo in op7418/guizang-ppt-skill nexu-io/open-design iamgio/quarkdown FormidableLabs/spectacle; do
  clone_or_pull "$repo"
done

# 1. Guizang PPT skill -> Claude Code skill (no build step)
rm -rf "$SKILLS_DIR/guizang-ppt-skill"
cp -r "$TOOLS_DIR/guizang-ppt-skill" "$SKILLS_DIR/guizang-ppt-skill"

# 2. OpenDesign deck/report skills -> Claude Code skills (plain SKILL.md, no daemon needed)
for s in data-report frontend-slides slides frame-data-chart-nyt design-consultation html-ppt-retro-quarterly-review; do
  rm -rf "$SKILLS_DIR/$s"; cp -r "$TOOLS_DIR/open-design/skills/$s" "$SKILLS_DIR/$s"
done

# QUICK=1 (used by the SessionStart hook): repos + skills only, skip the slow builds.
if [ "${QUICK:-0}" = "1" ]; then echo "Quick install done (skills only)."; exit 0; fi

# 3. OpenDesign app (Node 24 + pnpm 10.33 via corepack). Start with: pnpm tools-dev run web
if node -v | grep -q '^v24'; then
  (cd "$TOOLS_DIR/open-design" && corepack enable && corepack pnpm install)
else
  echo "SKIP open-design app: needs Node 24 (found $(node -v)). Run 'nvm install 24' then re-run." >&2
fi

# 4. Spectacle (React deck library). For a new deck: npx create-spectacle
(cd "$TOOLS_DIR/spectacle" && PUPPETEER_SKIP_DOWNLOAD=1 pnpm install --frozen-lockfile) \
  || echo "WARN spectacle install failed" >&2

# 5. Quarkdown CLI (official installer -> /opt/quarkdown, /usr/local/bin/quarkdown; needs Java 17+)
if ! command -v quarkdown >/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/quarkdown-labs/get-quarkdown/refs/heads/main/install.sh \
    | sudo env "PATH=$PATH" bash \
    || (cd "$TOOLS_DIR/quarkdown" && ./gradlew installDist && echo "Quarkdown built: $TOOLS_DIR/quarkdown/quarkdown-cli/build/install/quarkdown/bin")
fi

echo "Done. Skills in $SKILLS_DIR; repos in $TOOLS_DIR."
