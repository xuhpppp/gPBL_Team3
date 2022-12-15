module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/standard'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'space-before-function-paren':0,
    'no-unused-vars': 0,
    'space-before-function-paren': 0,
    'no-trailing-spaces': 0,
    'eol-last': 0,
    'no-multiple-empty-lines': 0,
    'vue/multi-word-component-names': 0
  }
}
