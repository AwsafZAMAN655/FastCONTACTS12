package com.example.fastcontacts

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.core.widget.doAfterTextChanged

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        val chkEmail = findViewById<CheckBox>(R.id.chkShowEmail)
        chkEmail.isChecked = Prefs.showEmail(this)
        chkEmail.setOnCheckedChangeListener { _, checked ->
            Prefs.setShowEmail(this@SettingsActivity, checked)
        }

        val chkSort = findViewById<CheckBox>(R.id.chkSortLast)
        chkSort.isChecked = Prefs.sortByLast(this)
        chkSort.setOnCheckedChangeListener { _, checked ->
            Prefs.setSortByLast(this@SettingsActivity, checked)
        }

        val etCode = findViewById<EditText>(R.id.etCountryCode)
        etCode.setText(Prefs.countryCode(this))
        etCode.doAfterTextChanged {
            Prefs.setCountryCode(this@SettingsActivity, it?.toString() ?: "")
        }

        findViewById<Button>(R.id.btnSyncSettings).setOnClickListener {
            try {
                startActivity(Intent(Settings.ACTION_SYNC_SETTINGS))
            } catch (e: Exception) {
                startActivity(Intent(Settings.ACTION_SETTINGS))
            }
        }
    }
}
