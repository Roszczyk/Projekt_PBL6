package com.example.hive

import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class HivesActivity : AppCompatActivity() {

    private var text: TextView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.hives_activity)

        // Odczytanie danych przekazanych z poprzedniej aktywności
        val hivesList = intent.getStringArrayListExtra("hivesData")

        val spinner: Spinner = findViewById(R.id.hivesSpinner)

        // Tworzenie adaptera dla spinnera
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, hivesList.orEmpty())

        // Określenie wyglądu rozwijanej listy spinnera
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        // Przypisanie adaptera do spinnera
        spinner.adapter = adapter

        // Nasłuchiwanie zdarzenia wyboru elementu w spinnerze
        spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val selectedHive = parent?.getItemAtPosition(position) as String
                Log.d("HivesActivity", "Selected hive: $selectedHive")
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                // Obsługa sytuacji, gdy nie został wybrany żaden element
            }
        }
    }



}