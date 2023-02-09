package br.com.hussan.automatedgarden

object Config {
    val topics = arrayOf(
        "ifpr/soil_sensor",
        "ifpr/temp_sensor",
        "ifpr/humidity_sensor",
        "ifpr/rain_sensor",
        "ifpr/water_control"
    )
    val qos = intArrayOf(1, 1, 1, 1, 1)
    const val presetCollection = "presets"
    const val BROKER_URL = "tcp://broker.hivemq.com:1883"
}