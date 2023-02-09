package br.com.hussan.automatedgarden

import android.util.Log
import com.google.firebase.firestore.DocumentReference
import com.google.firebase.firestore.FieldPath
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import com.google.firebase.firestore.QuerySnapshot

class FireStore {

    private val db: FirebaseFirestore = FirebaseFirestore.getInstance()

    fun get(
        collection: String,
        limit: Long = 30,
        onSuccess: (QuerySnapshot?) -> Unit
    ) {
        db.collection(collection)
            .orderBy(
                "timestamp",
                Query.Direction.DESCENDING
            )
            .limit(limit)
            .get()
            .addOnSuccessListener { result ->
                onSuccess(result)
            }
            .addOnFailureListener { exception ->
                Log.w("h2", "Error getting documents.", exception)
            }
    }

    fun add(
        collection: String,
        data: Map<String, Any>,
        onSuccess: (DocumentReference?) -> Unit
    ) {
        db.collection(collection)
            .add(data)
            .addOnSuccessListener { documentReference ->
                onSuccess(documentReference)
                Log.d("h2", "DocumentSnapshot added with ID: ${documentReference.id}")
            }
            .addOnFailureListener { e ->
                Log.w("h2", "Error adding document", e)
            }
    }
}