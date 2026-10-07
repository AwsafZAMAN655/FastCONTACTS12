package com.example.fastcontacts

import android.content.Context

object Prefs {
    private fun sp(c: Context) = c.getSharedPreferences("fast_contacts_prefs", Context.MODE_PRIVATE)

    fun showEmail(c: Context): Boolean = sp(c).getBoolean("show_email", true)
    fun setShowEmail(c: Context, v: Boolean) = sp(c).edit().putBoolean("show_email", v).apply()

    fun sortByLast(c: Context): Boolean = sp(c).getBoolean("sort_last", false)
    fun setSortByLast(c: Context, v: Boolean) = sp(c).edit().putBoolean("sort_last", v).apply()

    fun countryCode(c: Context): String = sp(c).getString("country_code", "") ?: ""
    fun setCountryCode(c: Context, v: String) = sp(c).edit().putString("country_code", v).apply()
}
