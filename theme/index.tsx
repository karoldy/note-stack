/**
 * NoteStack custom theme entry.
 *
 * Responsibilities:
 *  1. Load all theme CSS (via ./index.css)
 *  2. Apply the default theme on first visit
 *  3. Re-export all original Rspress theme components
 *
 * Theme switching is handled via `data-theme` attribute on <html>.
 * To switch themes programmatically:
 *
 *   import { applyTheme } from '../custom-theme/utils';
 *   applyTheme('ocean-depths');
 *
 * No built-in theme switcher UI is provided — this is intentional.
 * Add your own switcher component when needed.
 */

import './index.css';
import { useEffect } from 'react';
import { Layout as OriginalLayout } from '@rspress/core/theme-original';
import { themes } from '../custom-theme';

// Re-export all original theme components (Level 3 pattern)
export * from '@rspress/core/theme-original';

// ---------------------------------------------------------------------------
// Internal: apply default theme on first mount
// ---------------------------------------------------------------------------

// const DEFAULT_THEME = 'forest-canopy';

export function ThemeInit() {
  useEffect(() => {
    const root = document.documentElement;

    // Only set if no theme has been applied yet (e.g. by a head script)
    if (!root.hasAttribute('data-theme')) {
      root.setAttribute('data-theme', themes['midnight-galaxy'].id);
    }
  }, []);

  return null;
}

// ---------------------------------------------------------------------------
// Layout override — injects ThemeInit into the component tree
// ---------------------------------------------------------------------------

export function Layout() {
  return (
    <>
      {/* <ThemeInit /> */}
      <OriginalLayout />
    </>
  );
}
