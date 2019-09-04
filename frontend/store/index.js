import { mutationTypes as types, alertTypes } from '@/modules/stateTypes'

export const state = () => ({
  bra: null,
  nivoseStations: null,
  nivoseData: null,
  massifs: null,
  alerts: [],
  massifLoading: false,
  nivoStationLoading: false,
  nivoDataLoading: false,
  flowCaptLoading: false,
  braLoading: false
})

export const mutations = {
  [types.BRA_LOADED](state, newBra) {
    state.bra = newBra
  },
  [types.NIVOSE_STATION_LOADED](state, newNivoStations) {
    state.nivoseStations = newNivoStations
  },
  [types.NIVOSE_DATA_LOADED](state, newNivoData) {
    state.nivoseData = newNivoData
  },
  [types.MASSIFS_LOADED](state, newMassifs) {
    state.massifLoading = false
    state.massifs = newMassifs
  },
  [types.SET_ALERT](state, payload) {
    if (Object.keys(alertTypes).includes(payload.level)) {
      throw new Error('Unexpected alert message type. Aborting.')
    }
    state.alerts.push({
      level: payload.level,
      message: payload.message,
      duration: payload.duration || 10
    })
  },
  [types.DECREASE_ALERT_DURATION](state, message, newDuration) {
    state.alerts
      .filter((e) => e.message === message)
      .forEach((e) => {
        e.duration = newDuration
      })
  },
  [types.REMOVE_ALERT](state, message) {
    state.alerts = state.alerts.filter((e) => e.message !== message)
  },
  [types.TOGGLE_MASSIFS_LOADING](state) {
    state.massifLoading = !state.massifLoading
  },
  [types.TOGGLE_NIVOSE_DATA_LOADING](state) {
    state.nivoDataLoading = !state.nivoDataLoading
  },
  [types.TOGGLE_NIVOSE_STATION_LOADING](state) {
    state.nivoStationLoading = !state.nivoStationLoading
  },
  [types.TOGGLE_BRA_LOADING](state) {
    state.braLoading = !state.braLoading
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
  async fetchLastBraById({ commit }, massifId) {
    commit(types.TOGGLE_BRA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/bra/${massifId}/last`
      )
      commit(types.BRA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: JSON.stringify(e)
      })
    } finally {
      commit(types.TOGGLE_BRA_LOADING)
    }
  },
  async fetchNivoseStation({ commit }) {
    commit(types.TOGGLE_NIVOSE_STATION_LOADING)
    try {
      const res = await this.$axios.get(`${process.env.baseUrl}/nivo/stations`)
      commit(types.NIVOSE_STATION_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: JSON.stringify(e)
      })
    } finally {
      commit(types.TOGGLE_NIVOSE_STATION_LOADING)
    }
  },
  async fetchLastNivoseById({ commit }, nivoseStationId) {
    commit(types.NIVOSE_DATA_LOADING)
    try {
      const res = await this.$axios.get(
        `${process.env.baseUrl}/nivo/${nivoseStationId}/last`
      )
      commit(types.NIVOSE_DATA_LOADED, res.data)
    } catch (e) {
      commit(types.SET_ALERT, { level: alertTypes.DANGER, message: e })
    } finally {
      commit(types.TOGGLE_NIVOSE_DATA_LOADING)
    }
  }
}

export const getters = {
  braUrl(state) {
    if (state.bra) {
      return `${process.env.baseUrl}/bra/html/${state.bra.id}`
    }
    return null
  }
}
