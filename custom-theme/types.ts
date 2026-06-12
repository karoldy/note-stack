/**
 * Theme color tokens — maps to Rspress CSS custom properties.
 * @see https://rspress.rs/ui/vars
 */
export interface ThemeColorTokens {
  /** Primary brand color */
  brand: string;
  /** Lighter brand — hover states */
  brandLight: string;
  /** Very light brand — tints, backgrounds */
  brandLighter: string;
  /** Darker brand — active/pressed states */
  brandDark: string;
  /** Even darker brand */
  brandDarker: string;
  /** Transparent brand — subtle backgrounds */
  brandTint: string;

  /** Page background */
  bg: string;
  /** Soft background — cards, callouts */
  bgSoft: string;
  /** Muted background — inline code, secondary surfaces */
  bgMute: string;
  /** Alt background — code blocks, contrast areas */
  bgAlt: string;

  /** Primary text */
  text1: string;
  /** Secondary text */
  text2: string;
  /** Tertiary text — captions, meta */
  text3: string;
  /** Quaternary text — placeholders, disabled */
  text4: string;

  /** Link color */
  link: string;
  /** Link hover color */
  linkHover: string;

  /** Divider */
  divider: string;
  /** Light divider */
  dividerLight: string;

  /** Inline code text */
  textCode: string;
  /** Inline code background */
  textCodeBg: string;
  /** Inline code border */
  textCodeBorder: string;

  /** Code block background */
  codeBlockBg: string;
  /** Code block text */
  codeBlockColor: string;
  /** Code block border */
  codeBlockBorder: string;

  /** Home hero gradient secondary color */
  homeHeroSecondaryColor: string;
  /** Home page background gradient */
  homeBackgroundBg: string;
  /** Home feature card background */
  homeFeatureBg: string;
}

/**
 * Complete theme definition — light and dark variants of all tokens.
 */
export interface Theme {
  /** Unique theme identifier (kebab-case) */
  id: string;
  /** Human-readable theme name */
  name: string;
  /** Short description */
  description: string;
  /** Preview color swatch (CSS color) */
  previewColor: string;
  /** Light mode color tokens */
  light: ThemeColorTokens;
  /** Dark mode color tokens */
  dark: ThemeColorTokens;
  /** Font stack */
  fonts: {
    base: string;
    mono: string;
  };
}
