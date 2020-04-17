import moment from 'moment'
import {
  globalMutationTypes as types,
  globalActionsTypes as actionsTypes,
  alertTypes,
  mapMutationTypes,
} from '@/modules/stateTypes'

export const strict = false

export const state = () => ({
  braData: null,
  nivoStations: [],
  selectedNivoStation: null,
  nivoData: null,
  flowCaptStations: [],
  flowCaptData: null,
  selectedFlowCaptStation: null,
  massifs: [],
  alerts: [],
  massifLoading: false,
  nivoStationLoading: false,
  nivoDataLoading: false,
  flowCaptLoading: false,
  braLoading: false,
})

export const mutations = {
  [types.BRA_LOADED](state, newBra) {
    state.braData = newBra
  },
  [types.SET_SELECTED_BRA](state, bra) {
    state.braData = bra
  },
  [types.SET_SELECTED_NIVO_STATION](state, nivo) {
    state.selectedNivoStation = nivo
  },
  [types.SET_SELECTED_FLOWCAPT_STATION](state, flowcapt) {
    state.selectedFlowCaptStation = flowcapt
  },
  [types.NIVO_STATION_LOADED](state, newNivoStations) {
    state.nivoStations = newNivoStations
  },
  [types.NIVO_DATA_LOADED](state, newNivoData) {
    state.nivoData = newNivoData
  },
  [types.MASSIFS_LOADED](state, newMassifs) {
    state.massifs = newMassifs
  },
  [types.FLOWCAPT_STATION_LOADED](state, newFlowCapt) {
    state.flowCaptStations = newFlowCapt
  },
  [types.FLOWCAPT_DATA_LOADED](state, newFlowCapt) {
    state.flowCaptData = newFlowCapt
  },
  [types.SET_ALERT](state, payload) {
    if (Object.keys(alertTypes).includes(payload.level)) {
      throw new Error('Unexpected alert message type. Aborting.')
    }
    const beforeLength = state.alerts.length
    state.alerts.push({
      id: beforeLength + 1,
      level: payload.level,
      message: payload.message,
      duration: payload.duration || 10,
    })
  },
  [types.DECREASE_ALERT_DURATION](state, payload) {
    const alertIndexToDecrease = state.alerts
      .map((a) => a.id)
      .indexOf(payload.alert.id)
    if (alertIndexToDecrease > -1) {
      state.alerts[alertIndexToDecrease].duration = payload.newDuration
    } else {
      throw new Error('Fail to decrease alert duration. Fatal.')
    }
  },
  [types.REMOVE_ALERT](state, payload) {
    state.alerts = state.alerts.filter((e) => e.id !== payload.id)
  },
  [types.TOGGLE_MASSIFS_LOADING](state) {
    state.massifLoading = !state.massifLoading
  },
  [types.TOGGLE_NIVO_DATA_LOADING](state) {
    state.nivoDataLoading = !state.nivoDataLoading
  },
  [types.TOGGLE_NIVO_STATION_LOADING](state) {
    state.nivoStationLoading = !state.nivoStationLoading
  },
  [types.TOGGLE_BRA_LOADING](state) {
    state.braLoading = !state.braLoading
  },
  [types.TOGGLE_FLOWCAPT_LOADING](state) {
    state.flowCaptLoading = !state.flowCaptLoading
  },
}

export const actions = {
  async [actionsTypes.FETCH_MASSIFS]({ commit }) {
    commit(types.TOGGLE_MASSIFS_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/bra/massifs`)
      commit(types.MASSIFS_LOADED, res.data)
      commit(`map/${mapMutationTypes.SET_RAW_GEOJSON}`, {
        layerName: 'massifs',
        geojson: res.data,
      })
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_MASSIFS_LOADING)
    }
  },
  async [actionsTypes.FETCH_LAST_BRA_DATA]({ commit, dispatch }, massifId) {
    commit(types.TOGGLE_BRA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/bra/massifs/${massifId}/last`
      )
      dispatch(actionsTypes.SET_SELECTED_BRA, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e,
      })
    } finally {
      commit(types.TOGGLE_BRA_LOADING)
    }
  },
  async [actionsTypes.FETCH_NIVO_STATIONS]({ commit }) {
    commit(types.TOGGLE_NIVO_STATION_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/nivo/stations`)
      commit(types.NIVO_STATION_LOADED, res.data)
      commit(`map/${mapMutationTypes.SET_RAW_GEOJSON}`, {
        layerName: 'posteNivo',
        geojson: res.data,
      })
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e,
      })
    } finally {
      commit(types.TOGGLE_NIVO_STATION_LOADING)
    }
  },
  [actionsTypes.SET_SELECTED_BRA]({ commit }, bra) {
    commit(types.SET_SELECTED_BRA, bra)
    commit('map/' + mapMutationTypes.SET_SELECTED_MASSIF, bra.massif)
  },
  [actionsTypes.SET_SELECTED_NIVO_STATION]({ commit }, nivo) {
    commit(types.SET_SELECTED_NIVO_STATION, nivo)
    commit('map/' + mapMutationTypes.SET_SELECTED_NIVO_STATION, nivo)
  },
  [actionsTypes.SET_SELECTED_FLOWCAPT_STATION]({ commit }, flowcapt) {
    commit(types.SET_SELECTED_FLOWCAPT_STATION, flowcapt)
    commit('map/' + mapMutationTypes.SET_SELECTED_FLOWCAPT_STATION, flowcapt)
  },
  async fetchNivoRecordsByStationId({ commit }, nivoStationId) {
    commit(types.TOGGLE_NIVO_DATA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/nivo/stations/${nivoStationId}/records`
      )
      commit(types.NIVO_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_NIVO_DATA_LOADING)
    }
  },
  async fetchLastNivoById({ commit }, nivoStationId) {
    commit(types.TOGGLE_NIVO_DATA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/nivo/stations/${nivoStationId}/records/last`
      )
      commit(types.NIVO_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_NIVO_DATA_LOADING)
    }
  },
  async [actionsTypes.FETCH_FLOWCAPT_STATIONS]({ commit }) {
    commit(types.TOGGLE_FLOWCAPT_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/flowcapt/stations`
      )
      commit(types.FLOWCAPT_STATION_LOADED, res.data)
      commit(`map/${mapMutationTypes.SET_RAW_GEOJSON}`, {
        layerName: 'flowcapt',
        geojson: res.data,
      })
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e,
      })
    } finally {
      commit(types.TOGGLE_FLOWCAPT_LOADING)
    }
  },
  async [actionsTypes.FETCH_FLOWCAPT_DATA]({ commit }, stationId) {
    commit(types.TOGGLE_FLOWCAPT_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/flowcapt/measures/${stationId}`
      )
      commit(types.FLOWCAPT_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e,
      })
    } finally {
      commit(types.TOGGLE_FLOWCAPT_LOADING)
    }
  },
}

export const getters = {
  braUrl(state) {
    if (state.braData) {
      return `${process.env.baseUrl}/bra/html/${state.braData.id}`
    }
    return null
  },
  braDate(state) {
    if (state.braData) {
      return moment(state.braData.production_date).format('YYYY-MM-DD')
    }
    return null
  },
}
