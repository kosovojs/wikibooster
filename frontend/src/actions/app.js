export const SET_WIKI_LANGUAGE = 'SET_WIKI_LANGUAGE';

export const setWikiLanguage = (language) => ({
	type: SET_WIKI_LANGUAGE,
	language
});

export const SET_WIKI_OPTIONS = 'SET_WIKI_OPTIONS';

export const setWikiOptions = (data) => ({
	type: SET_WIKI_OPTIONS,
	data
});

export const NULLIFY_APP_STATE = 'NULLIFY_APP_STATE';

export const nullifyAppState = () => ({
	type: NULLIFY_APP_STATE
});