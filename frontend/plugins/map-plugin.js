/**
 * Storing Openlayers objects (or any other complex objects) in vuex is a bad practice and breaks
 * dev tools.
 * This plugin instanciate a Map Layer service which
 */

import MapService from './map-service'

export default (context, inject) => {
  inject('mapService', new MapService(context.store))
}
