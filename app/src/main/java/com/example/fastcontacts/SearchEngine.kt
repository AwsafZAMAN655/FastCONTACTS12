package com.example.fastcontacts

class SearchEngine(private val contacts: List<Contact>) {

    fun search(query: String): List<Contact> {
        val q = query.lowercase().trim()
        if (q.isBlank()) return contacts
        val qDigits = q.filter { it.isDigit() }

        val scored = ArrayList<Pair<Int, Contact>>()
        for (c in contacts) {
            val tier = calculateTier(c, q, qDigits)
            if (tier >= 0) {
                scored.add(Pair(tier, c))
            }
        }

        return scored
            .sortedWith(
                compareBy<Pair<Int, Contact>>(
                    { it.first },
                    { it.second.firstName.lowercase() },
                    { it.second.name.lowercase() }
                )
            )
            .map { it.second }
    }

    private fun calculateTier(c: Contact, q: String, qDigits: String): Int {
        val first = c.firstName.lowercase().trim()
        val last = c.lastName.lowercase().trim()
        val full = c.name.lowercase().trim()

        return when {
            first == q -> 0
            first.startsWith(q) -> 1
            first.contains(q) -> 2
            last.isNotEmpty() && last.startsWith(q) -> 3
            full.startsWith(q) -> 4
            full.contains(q) -> 5
            qDigits.isNotEmpty() && c.phones.any { p ->
                p.number.filter { it.isDigit() }.contains(qDigits)
            } -> 6
            c.emails.any { it.address.lowercase().contains(q) } -> 7
            else -> -1
        }
    }

    companion object {
        fun sorted(list: List<Contact>, byLast: Boolean): List<Contact> {
            return list.sortedWith(compareBy(
                { key(it, byLast) },
                { it.name.lowercase() }
            ))
        }

        private fun key(c: Contact, byLast: Boolean): String {
            return if (byLast) {
                val primary = c.lastName.ifBlank { c.firstName }
                (primary + " " + c.firstName).lowercase()
            } else {
                c.name.lowercase()
            }
        }

        fun letterOf(c: Contact, byLast: Boolean): String {
            val k = key(c, byLast).trim()
            val ch = k.firstOrNull() ?: return "#"
            return if (ch.isLetter()) ch.uppercase() else "#"
        }
    }
}
