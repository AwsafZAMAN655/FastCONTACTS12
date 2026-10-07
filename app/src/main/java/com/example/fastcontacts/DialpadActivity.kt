package com.example.fastcontacts

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.GridLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton

class DialpadActivity : AppCompatActivity() {

    private val number = StringBuilder()
    private lateinit var display: TextView
    private lateinit var adapter: ContactAdapter
    private var engine = SearchEngine(emptyList())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dialpad)

        display = findViewById(R.id.dialDisplay)

        adapter = ContactAdapter(
            onClick = { c ->
                val i = Intent(this, DetailActivity::class.java)
                i.putExtra("contact_id", c.id)
                startActivity(i)
            },
            onCallClick = { c -> Actions.withNumber(this, c) { n -> Actions.call(this, n) } },
            onSmsClick = { c -> Actions.withNumber(this, c) { n -> Actions.sms(this, n) } }
        )
        val suggestions = findViewById<RecyclerView>(R.id.suggestions)
        suggestions.layoutManager = LinearLayoutManager(this)
        suggestions.adapter = adapter

        buildKeypad()

        findViewById<Button>(R.id.btnDialCall).setOnClickListener {
            if (number.isNotEmpty()) Actions.call(this, number.toString())
        }
        findViewById<Button>(R.id.btnAddContact).setOnClickListener {
            if (number.isNotEmpty()) Actions.create(this, number.toString())
        }
        val back = findViewById<Button>(R.id.btnBackspace)
        back.setOnClickListener {
            if (number.isNotEmpty()) number.deleteCharAt(number.length - 1)
            refresh()
        }
        back.setOnLongClickListener {
            number.setLength(0)
            refresh()
            true
        }
        refresh()
    }

    override fun onResume() {
        super.onResume()
        Thread {
            val loaded = ContactsRepository.loadAll(this)
            runOnUiThread {
                engine = SearchEngine(SearchEngine.sorted(loaded, false))
                refresh()
            }
        }.start()
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()

    private fun buildKeypad() {
        val keypad = findViewById<GridLayout>(R.id.keypad)
        val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#")
        for (k in keys) {
            val b = MaterialButton(this)
            b.text = k
            b.textSize = 24f
            val lp = GridLayout.LayoutParams(
                GridLayout.spec(GridLayout.UNDEFINED),
                GridLayout.spec(GridLayout.UNDEFINED, 1f)
            )
            lp.width = 0
            lp.height = dp(64)
            lp.setMargins(dp(4), dp(4), dp(4), dp(4))
            b.layoutParams = lp
            b.setOnClickListener {
                number.append(k)
                refresh()
            }
            if (k == "0") {
                b.setOnLongClickListener {
                    number.append("+")
                    refresh()
                    true
                }
            }
            keypad.addView(b)
        }
    }

    private fun refresh() {
        display.text = number.toString()
        if (number.isEmpty()) {
            adapter.submit(emptyList())
        } else {
            adapter.submit(engine.search(number.toString()).take(20))
        }
    }
}
