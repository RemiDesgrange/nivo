import Style from 'ol/style/Style'
import Fill from 'ol/style/Fill'
import Stroke from 'ol/style/Stroke'
import Point from 'ol/geom/Point'
import pointOnFeature from '@turf/point-on-feature'
import Circle from 'ol/geom/Circle'
import CircleStyle from 'ol/style/Circle'

/**
 * @param {number|number[]} lonOrCoordinates
 * @param {number} [lat]
 * @return {Point}
 * @private
 */
function createPointGeom(lonOrCoordinates, lat) {
  const coordinates = Array.isArray(lonOrCoordinates)
    ? lonOrCoordinates
    : [lonOrCoordinates, lat]

  return new Point(coordinates)
}

/**
 * @param {Geometry|Object} geom
 * @return {SimpleGeometry|Object}
 * @throws {Error}
 * @private
 */
function toSimpleGeom(geom) {
  if (geom instanceof Circle) {
    geom = createPointGeom(geom.getCenter())
  }
  const type = geom.type || geom.getType()
  const complexTypes = ['GeometryCollection']
  if (complexTypes.includes(type) === false) {
    return geom
  }
  return (geom.geometries || geom.getGeometries())[0]
}

/**
 * @param {Geometry|Object} geom
 * @return {Coordinate|undefined}
 */
export function findPointOnSurface(geom) {
  const simpleGeom = toSimpleGeom(geom)
  const pointFeature = pointOnFeature({
    type: simpleGeom.type || simpleGeom.getType(),
    coordinates: simpleGeom.coordinates || simpleGeom.getCoordinates(),
  })

  if (pointFeature && pointFeature.geometry) {
    return pointFeature.geometry.coordinates
  }
}

/**
 *
 * @param {Feature} feature
 * @returns {Style}
 */
export function selectionStyleBasedOnExisting(feature) {
  // takes an existing styles and make it sligthly bigger when selected.
  const existingStyle = feature.getStyle()
  if (existingStyle instanceof Style) {
    const stroke = existingStyle.getStroke()
    stroke.setWidth(stroke.getWidth() + 3)
    return new Style({
      stroke,
      fill: existingStyle.getFill(),
    })
  }
}

/**
 *
 * @param {string} color
 * @param {Number|string} opacity
 * @returns {string}
 * @private
 */
function _setOpacityInRGBA(color, opacity) {
  const newcol = color.split(',')
  newcol.pop()
  newcol.push(` ${opacity})`)
  return newcol.join(',')
}

/**
 *
 * @param {Feature} feature
 * @returns {Style}
 */
export function massifsStyleFunc(feature) {
  const risk = feature.get('latest_record').max_risk
  const color = {
    '5': 'rgba(254, 5, 0, 1)',
    '4': 'rgba(254, 35, 32, 1)',
    '3': 'rgba(255, 158, 1, 1)',
    '2': 'rgba(254, 255, 0, 1)',
    '1': 'rgba(205, 255, 96, 1)',
  }
  const index = Object.keys(color).find((e) => Number(e) === risk)
  let currentRiskColor = null
  if (index === undefined) {
    currentRiskColor = 'rgba(86, 130, 243, 1)'
  } else {
    currentRiskColor = color[index]
  }

  return new Style({
    fill: new Fill({
      color: _setOpacityInRGBA(currentRiskColor, 0.5),
    }),
    stroke: new Stroke({
      color: currentRiskColor,
      width: 2,
    }),
  })
}

/**
 *
 * @param {Feature} feature
 * @returns {Style}
 */
export function nivoStationStyleFunc(feature) {
  return new Style({
    image: new CircleStyle({
      radius: 5,
      fill: new Fill({
        color: 'rgba(255, 255, 255, 0.3)',
      }),
      stroke: new Stroke({
        color: 'rgba(254, 5, 0, 1)',
        width: 2,
      }),
    }),
  })
}
