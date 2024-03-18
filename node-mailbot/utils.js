export function cookiesToString(cookies) {
  if (!cookies) return '';
  return Object.keys(cookies).reduce((prev, key) => {
    return `${prev}${cookies[key].split(';')[0]}; `;
  }, '');
}

