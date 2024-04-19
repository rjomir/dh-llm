const arr = [
  {
    name: 'OPEN_AI_KEY',
    value: '',
    secret: true,
    tab: 'General',
  },
  {
    name: 'OPEN_AI_MODEL',
    value: 'gpt-3.5-turbo-instruct',
    secret: false,
    tab: 'General',
  },
  {
    name: 'OPEN_AI_MAX_TOKENS',
    value: '400',
    secret: false,
    tab: 'General',
  },
  {
    name: 'BERT_SCORE_SAMPLING_NUMBER',
    value: '4',
    secret: false,
    tab: 'Bert score',
  },
  {
    name: 'NGRAM_SAMPLING_NUMBER',
    value: '4',
    secret: false,
    tab: 'N-gram',
  },
  {
    name: 'CHAINPOLL_SAMPLING_NUMBER',
    value: '5',
    secret: false,
    tab: 'Chainpoll',
  },
  {
    name: 'SERPER_API_KEY',
    value: '',
    secret: true,
    tab: 'RefChecker'
  }
];

export const defaultFormState = () => {
  let state = {};
  arr.forEach((element) => (state[element.name] = element.value));
  return state;
};
export const settings = Object.groupBy(arr, ({ tab }) => tab);
export const settingsTabs = Object.keys(settings).map((key, index) => ({
  name: key,
  value: index,
}));
