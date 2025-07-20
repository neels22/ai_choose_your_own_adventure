// URL.canParse polyfill for compatibility
if (typeof URL !== 'undefined' && !URL.canParse) {
  URL.canParse = function(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };
}

export const API_BASE_URL = "http://localhost:8000/api";