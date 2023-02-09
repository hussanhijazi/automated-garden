package br.com.hussan.automatedgarden

import android.content.Context
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import br.com.hussan.automatedgarden.databinding.ActivityMainBinding
import br.com.hussan.automatedgarden.model.Sensor
import br.com.hussan.automatedgarden.model.SensorValue
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import org.eclipse.paho.client.mqttv3.MqttMessage

class MessageHandler(private val sensors: List<Sensor>) {

    fun handle(
        context: Context,
        binding: ActivityMainBinding,
        topic: String,
        message: MqttMessage
    ) {

    }
}