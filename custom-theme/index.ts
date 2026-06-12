/**
 * NoteStack Custom Theme Collection
 *
 * Usage:
 *   import { themes, themeIds } from '../custom-theme';
 *   import { applyTheme } from '../custom-theme/utils';
 *
 *   // Get a specific theme
 *   const theme = themes['forest-canopy'];
 *
 *   // Switch theme at runtime
 *   applyTheme('forest-canopy');
 */

export type { Theme, ThemeColorTokens } from './types';

export { forestCanopy } from './forest-canopy/index';
export { oceanDepths } from './ocean-depths/index';
export { techInnovation } from './tech-innovation/index';
export { midnightGalaxy } from './midnight-galaxy/index';

import { forestCanopy } from './forest-canopy/index';
import { oceanDepths } from './ocean-depths/index';
import { techInnovation } from './tech-innovation/index';
import { midnightGalaxy } from './midnight-galaxy/index';
import type { Theme } from './types';

/** All available themes keyed by id */
export const themes: Record<string, Theme> = {
  [forestCanopy.id]: forestCanopy,
  [oceanDepths.id]: oceanDepths,
  [techInnovation.id]: techInnovation,
  [midnightGalaxy.id]: midnightGalaxy,
};

/** Ordered list of theme ids */
export const themeIds: string[] = [
  forestCanopy.id,
  oceanDepths.id,
  techInnovation.id,
  midnightGalaxy.id,
];

/** Default theme applied on first visit */
export const defaultThemeId = forestCanopy.id;
