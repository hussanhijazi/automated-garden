package br.com.hussan.automatedgarden

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class MyFirebaseMessageService: FirebaseMessagingService() {

    private val fireStore = FireStore()

    companion object {
        const val CHANNEL_ID = "AUTOMATED_GARDEN"
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        createNotificationChannel()

        remoteMessage.notification?.let {
            Log.d("h21", it.title.toString())
            Log.d("h2", it.body.toString())
            var builder = NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_launcher_background)
                .setContentTitle(it.title)
                .setContentText(it.body)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)

            with(NotificationManagerCompat.from(this)) {
                // notificationId is a unique int for each notification that you must define
                notify(NotificationID.ID, builder.build())
            }
        }
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        val userToken = mapOf<String, Any>("token" to token)
        fireStore.add("users_tokens", userToken, {})
        Log.d("h2", token)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = CHANNEL_ID
            val descriptionText = CHANNEL_ID
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
}