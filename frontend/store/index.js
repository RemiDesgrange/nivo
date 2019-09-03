const types = {
  BRA_LOADING: 'BRA_LOADING',
  BRA_LOADED: 'BRA_LOADED',
  MASSIFS_LOADING: 'MASSIFS_LOADING',
  MASSIFS_LOADED: 'MASSIFS_LOADED',
  NIVOSE_DATA_LOADING: 'NIVOSE_DATA_LOADING',
  NIVOSE_DATA_LOADED: 'NIVOSE_DATA_LOADED',
  NIVOSE_STATION_LOADING: 'NIVOSE_STATION_LOADING',
  NIVOSE_STATION_LOADED: 'NIVOSE_STATION_LOADED',
  FLOWCAPT_LOADING: 'FLOWCAPT_LOADING',
  FLOWCAPT_LOADED: 'FLOWCAPT_LOADED',
  SET_ERROR: 'SET_ERROR'
}

export const state = () => ({
  bra: null,
  nivoseStations: null,
  nivoseData: null,
  massifs: null,
  errors: [],
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
    state.nivoStationLoading = false
    state.nivoseStations = newNivoStations
  },
  [types.NIVOSE_DATA_LOADED](state, newNivoData) {
    state.nivoDataLoading = false
    state.nivoseData = newNivoData
  },
  [types.MASSIFS_LOADED](state, newMassifs) {
    state.massifLoading = false
    state.massifs = newMassifs
  },
  [types.SET_ERROR](state, error) {
    state.errors.push(error)
  },
  [types.MASSIFS_LOADING](state) {
    state.massifLoading = !state.massifLoading
  },
  [types.NIVOSE_DATA_LOADING](state) {
    state.nivoDataLoading = !state.nivoDataLoading
  },
  [types.NIVOSE_STATION_LOADING](state) {
    state.nivoStationLoading = !state.nivoStationLoading
  },
  [types.BRA_LOADING](state) {
    state.braLoading = !state.braLoading
  }
}

export const actions = {
  // this special actions is executed when server starts
  async nuxtServerInit({ dispatch }) {
    await dispatch('fetchMassifs')
    await dispatch('fetchNivoseStation')
  },
  async fetchMassifs({ commit }) {
    commit(types.MASSIFS_LOADING)
    const res = await this.$axios.get(`${process.env.baseUrl}/bra/massifs`)
    commit(types.MASSIFS_LOADED, res.data)
  },
  fetchLastBraById({ commit }, massifId) {
    commit(types.BRA_LOADING)
    this.$axios
      .get(`${process.env.baseUrl}/bra/${massifId}/last`)
      .then((res) => {
        commit(types.BRA_LOADED, res.data)
      })
      .catch((e) => {
        commit(types.BRA_LOADING)
        commit(types.SET_ERROR, e)
      })
  },
  async fetchNivoseStation({ commit }) {
    commit(types.NIVOSE_STATION_LOADING)
    const res = await this.$axios.get(`${process.env.baseUrl}/nivo/stations`)
    commit(types.NIVOSE_STATION_LOADED, res.data)
  },
  fetchLastNivoseById({ commit }, nivoseStationId) {
    commit(types.NIVOSE_DATA_LOADING)
    this.$axios
      .get(`${process.env.baseUrl}/nivo/${nivoseStationId}/last`)
      .then((res) => {
        commit(types.NIVOSE_DATA_LOADED, res.data)
      })
      .catch((e) => {
        commit(types.SET_ERROR, e)
        commit(types.NIVOSE_DATA_LOADING)
      })
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
