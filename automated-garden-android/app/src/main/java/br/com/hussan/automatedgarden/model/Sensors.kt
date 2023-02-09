package br.com.hussan.automatedgarden.model

import br.com.hussan.automatedgarden.Config
import br.com.hussan.automatedgarden.databinding.ActivityMainBinding

class Sensors(val binding: ActivityMainBinding) {
    val soilSensor = Sensor(name = "Umidade do solo", topic = Config.topics[0],
        collection = "ifpr_soil_sensor", chartView = binding.chartSoil)
    val tempSensor = Sensor(name = "Temperatura do ar", topic = Config.topics[1],
        collection = "ifpr_temp_sensor", chartView = binding.chartTempAir)
    val humiditySensor = Sensor(name = "Umidade do ar", topic = Config.topics[2],
        collection = "ifpr_humidity_sensor", chartView = binding.chartHumidityAir)
    val rainSensor = Sensor(name = "Chuva", topic = Config.topics[3],
        collection = "ifpr_rain_sensor", chartView = binding.chartRain)

    val sensors by lazy {
        listOf(soilSensor, tempSensor, humiditySensor, rainSensor)
    }
}