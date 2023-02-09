package br.com.hussan.automatedgarden

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.graphics.Color
import android.os.Build
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.core.content.ContextCompat.getSystemService
import br.com.hussan.automatedgarden.Config.BROKER_URL
import java.util.*
import org.eclipse.paho.android.service.MqttAndroidClient
import org.eclipse.paho.client.mqttv3.IMqttActionListener
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken
import org.eclipse.paho.client.mqttv3.IMqttToken
import org.eclipse.paho.client.mqttv3.MqttCallback
import org.eclipse.paho.client.mqttv3.MqttException
import org.eclipse.paho.client.mqttv3.MqttMessage

/**
 * topic_temp = b'ifpr/temp_sensor'
topic_humidity = b'ifpr/humidity_sensor'
topic_soil = b'ifpr/soil_sensor'
topic_rain = b'ifpr/rain_sensor'

topic_water = b'ifpr/water_control'

mqtt_broker = 'broker.hivemq.com'
water_state_collection = "water_state"

mqtt_config = {
'mqtt_broker': mqtt_broker,
'port': 1883,
'client_id': b'automated-garden'
}

 */

class MqttClient(private val onMessage: (topic: String, message: MqttMessage) -> Unit) {
    private lateinit var mqttAndroidClient: MqttAndroidClient

    fun connect(
        applicationContext: Context,
        onSuccess: () -> Unit,
        onFailure: () -> Unit
    ) {
        mqttAndroidClient = MqttAndroidClient(applicationContext,
            BROKER_URL,
            UUID.randomUUID().toString()
        )

        try {
            val token = mqttAndroidClient.connect()
            token.actionCallback = object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken) {
                    onSuccess()
                }
                override fun onFailure(asyncActionToken: IMqttToken, exception: Throwable) {
                    Log.i("h2", "failure")
                    onFailure()
                    exception.printStackTrace()
                }
            }
        } catch (e: MqttException) {
            e.printStackTrace()
        }
    }

    fun subscribe(
        topics: Array<String>,
        qos: IntArray,
        onSuccess: () -> Unit,
        onFailure: () -> Unit
    ) {
        try {
            mqttAndroidClient.subscribe(
                topics,
                qos,
                null,
                object : IMqttActionListener {
                    override fun onSuccess(asyncActionToken: IMqttToken) {
                        onSuccess()
                    }

                    override fun onFailure(
                        asyncActionToken: IMqttToken,
                        exception: Throwable
                    ) {
                        Log.d("h2", exception.toString())
                        onFailure()
                    }
                })
        } catch (e: MqttException) {
            // Give your subscription failure callback here
        }
    }

    fun unSubscribe(topic: String) {
        try {
            val unsubToken = mqttAndroidClient.unsubscribe(topic)
            unsubToken.actionCallback = object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken) {
                    // Give your callback on unsubscribing here
                }

                override fun onFailure(asyncActionToken: IMqttToken, exception: Throwable) {
                    // Give your callback on failure here
                }
            }
        } catch (e: MqttException) {
            // Give your callback on failure here
        }
    }

    fun receiveMessages() {
        mqttAndroidClient.setCallback(object : MqttCallback {
            override fun connectionLost(cause: Throwable?) {
                //connectionStatus = false
                // Give your callback on failure here
            }

            override fun messageArrived(topic: String, message: MqttMessage) {
                try {
                    // data is the desired received message
                    // Give your callback on message received here
                    onMessage(topic, message)
                } catch (e: Exception) {
                    // Give your callback on error here
                }
            }

            override fun deliveryComplete(token: IMqttDeliveryToken) {
                // Acknowledgement on delivery complete
            }
        })
    }

    fun publish(topic: String, data: String) {
        val encodedPayload: ByteArray
        try {
            encodedPayload = data.toByteArray(charset("UTF-8"))
            val message = MqttMessage(encodedPayload)
            message.qos = 2
            message.isRetained = false
            mqttAndroidClient.publish(topic, message)
        } catch (e: Exception) {
            // Give Callback on error here
        } catch (e: MqttException) {
            // Give Callback on error here
        }
    }

    fun disconnect() {
        try {
            val disconToken = mqttAndroidClient.disconnect()
            disconToken.actionCallback = object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken) {
                    //connectionStatus = false
                    // Give Callback on disconnection here
                    Log.d("h2", "disconnect")
                }

                override fun onFailure(
                    asyncActionToken: IMqttToken,
                    exception: Throwable
                ) {
                    // Give Callback on error here
                    Log.d("h2", exception.toString())
                }
            }
        } catch (e: MqttException) {
            Log.d("h2", e.toString())
            // Give Callback on error here
        }
    }


}