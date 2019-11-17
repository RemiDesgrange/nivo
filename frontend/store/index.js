import { mutationTypes as types, alertTypes } from '@/modules/stateTypes'

export const state = () => ({
  selectedBra: null,
  braData: [],
  nivoStations: [],
  nivoData: null,
  flowCaptStations: [],
  flowCaptData: null,
  massifs: [],
  alerts: [],
  massifLoading: false,
  nivoStationLoading: false,
  nivoDataLoading: false,
  flowCaptLoading: false,
  braLoading: false
})

export const mutations = {
  [types.BRA_LOADED](state, newBra) {
    state.braData = newBra
  },
  [types.SET_SELECTED_BRA](state, bra) {
    state.selectedBra = bra
  },
  [types.NIVO_STATION_LOADED](state, newNivoStations) {
    state.nivoStations = newNivoStations
  },
  [types.NIVO_DATA_LOADED](state, newNivoData) {
    state.nivoData = newNivoData
  },
  [types.MASSIFS_LOADED](state, newMassifs) {
    state.massifLoading = false
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
      duration: payload.duration || 10
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
  }
}

export const actions = {
  async fetchMassifs({ commit }) {
    commit(types.TOGGLE_MASSIFS_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/bra/massifs`)
      commit(types.MASSIFS_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_MASSIFS_LOADING)
    }
  },
  async fetchLastBraData({ commit }) {
    commit(types.TOGGLE_BRA_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/bra/last`)
      commit(types.BRA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e
      })
    } finally {
      commit(types.TOGGLE_BRA_LOADING)
    }
  },
  async fetchNivoStation({ commit }) {
    commit(types.TOGGLE_NIVO_STATION_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/nivo/stations`)
      commit(types.NIVO_STATION_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e
      })
    } finally {
      commit(types.TOGGLE_NIVO_STATION_LOADING)
    }
  },
  async fetchLastNivoById({ commit }, nivoStationId) {
    commit(types.NIVO_DATA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/nivo/${nivoStationId}/last`
      )
      commit(types.NIVO_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_NIVO_DATA_LOADING)
    }
  },
  async fetchFlowCaptStation({ commit }) {
    commit(types.TOGGLE_FLOWCAPT_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/flowcapt/stations`
      )
      commit(types.FLOWCAPT_STATION_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e
      })
    } finally {
      commit(types.TOGGLE_FLOWCAPT_LOADING)
    }
  },
  async fetchFlowCaptData({ commit }, stationId) {
    commit(types.TOGGLE_FLOWCAPT_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/flowcapt/measures/with_timestamp/${stationId}`
      )
      commit(types.FLOWCAPT_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: e
      })
    } finally {
      commit(types.TOGGLE_FLOWCAPT_LOADING)
    }
  }
}

export const getters = {
  braUrl(state) {
    if (state.selectedBra) {
      return `${process.env.baseUrl}/bra/html/${state.selectedBra.id}`
    }
    return null
  }
}
