export const gloablMutationTypes = {
  SET_ALERT: 'SET_ALERT',
  SET_SELECTED_BRA: 'SET_SELECTED_BRA',
  SET_SELECTED_NIVO_STATION: 'SET_SELECTED_NIVO_STATION',
  DECREASE_ALERT_DURATION: 'DECREASE_ALERT_DURATION',
  REMOVE_ALERT: 'REMOVE_ALERT',
  TOGGLE_MASSIFS_LOADING: 'TOGGLE_TOGGLE_MASSIFS_LOADING',
  TOGGLE_NIVO_DATA_LOADING: 'TOGGLE_NIVO_DATA_LOADING',
  TOGGLE_FLOWCAPT_LOADING: 'TOGGLE_FLOWCAPT_LOADING',
  TOGGLE_NIVO_STATION_LOADING: 'TOGGLE_NIVO_STATION_LOADING',
  TOGGLE_BRA_LOADING: 'BRA_LOADING',
  // Loading mutations
  BRA_LOADED: 'BRA_LOADED',
  MASSIFS_LOADED: 'MASSIFS_LOADED',
  NIVO_DATA_LOADED: 'NIVO_DATA_LOADED',
  NIVO_STATION_LOADED: 'NIVO_STATION_LOADED',
  FLOWCAPT_STATION_LOADED: 'FLOWCAPT_STATION_LOADED',
  FLOWCAPT_DATA_LOADED: 'FLOWCAPT_DATA_LOADED',
}

export const globalActionsTypes = {
  FETCH_MASSIFS: 'FETCH_MASSIFS',
}

export const alertTypes = {
  PRIMARY: 'primary',
  SECONDARY: 'secondary',
  SUCCESS: 'success',
  DANGER: 'danger',
  WARNING: 'warning',
  INFO: 'info',
  LIGHT: 'light',
  DARK: 'dark',
}

export const mapGettersTypes = {
  GET_LAYERS: 'GET_LAYERS',
  GET_BASE_LAYERS: 'GET_BASE_LAYERS',
  SELECTED_BASE_LAYER: 'SELECTED_BASE_LAYER',
  SELECTED_NIVO_STATION: 'SELECTED_NIVO_STATION',
  SELECTED_FLOWCAPT_STATION: 'SELECTED_FLOWCAPT_STATION',
  SELECTED_MASSIF: 'SELECTED_MASSIF',
  SELECTED_NIVO_STATION_HOVER: 'SELECTED_NIVO_STATION_HOVER',
  SELECTED_NIVO_STATION_CLICK: 'SELECTED_NIVO_STATION_CLICK',
  SELECTED_FLOWCAPT_STATION_HOVER: 'SELECTED_FLOWCAPT_STATION_HOVER',
  SELECTED_FLOWCAPT_STATION_CLICK: 'SELECTED_FLOWCAPT_STATION_CLICK',
  SELECTED_MASSIF_HOVER: 'SELECTED_MASSIF_HOVER',
  SELECTED_MASSIF_CLICK: 'SELECTED_MASSIF_CLICK',
  SELECTED_NIVO_STATION_ALTITUDE_HOVER: 'SELECTED_NIVO_STATION_ALTITUDE_HOVER',
  SELECTED_NIVO_STATION_ALTITUDE_CLICK: 'SELECTED_NIVO_STATION_ALTITUDE_CLICK',
}

export const mapMutationTypes = {
  CREATE_MAP: 'CREATE_MAP',
  SET_VIEW: 'SET_VIEW',
  SET_TARGET: 'SET_TARGET',
  ADD_LAYER: 'ADD_LAYER',
  REMOVE_LAYER: 'REMOVE_LAYER',
  ADD_OVERLAY: 'ADD_OVERLAY',
  REMOVE_OVERLAY: 'REMOVE_OVERLAY',
  SET_OVERLAY_POSITION: 'SET_OVERLAY_POSITION',
  ADD_INTERACTION: 'ADD_INTERACTION',
  REMOVE_INTERACTION: 'REMOVE_INTERACTION',
  FIT_VIEW: 'FIT_VIEW',
  CLEAN_SELECTED_FEATURES: 'CLEAN_SELECTED_FEATURES',
  ADD_FEATURES: 'ADD_FEATURES',
  ADD_FEATURE: 'ADD_FEATURE',
  SET_FEATURES: 'SET_FEATURES',
  SET_FEATURE: 'SET_FEATURE',
  SET_RAW_GEOJSON: 'SET_RAW_GEOJSON',
  SET_SELECTED_BASE_LAYER: 'SET_SELECTED_BASE_LAYER',
  SET_SLOPES_VISIBILITY: 'SET_SLOPES_VISIBILITY',
  SET_SLOPES_OPACITY: 'SET_SLOPES_OPACITY',
}

export const mapActionsTypes = {
  INIT_MAP: 'INIT_MAP',
  ADD_FEATURES: 'ADD_FEATURES',
}
