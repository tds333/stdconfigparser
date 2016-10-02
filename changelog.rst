Changelog
=========

0.7
---

- Allow ':' as option (key) value separator. Still the advice is to use '='
  as default. But support the variant to parse more INI styles. Also ':' is
  not allowed in a option name. Now this is explicit.


0.6
---

- Make interpolation optional. As default disable it.
- Remove JSON converter. Can still be added as a custom converter with one line.
- Add compatibility for Python 3.3 and Python 3.4.


0.5
---

- Make StdConfigParser available in __all__.
- Remove encoding parameter in method read(). Make fixed use of utf-8.
- Add support for ':' in section interpolation.


0.4
---

Initial release