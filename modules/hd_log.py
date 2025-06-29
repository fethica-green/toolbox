# modules/hd_log.py

import streamlit as st

def render():
    st.header("📖 RÉSUMÉ OPÉRATIONNEL – PROCÉDURES LOGISTIQUES HD – MENA")

    # Section 1
    with st.expander("1. VOYAGES ET MISSIONS", expanded=True):
        st.markdown("""
- **Travel Authorization (TA)**  
  Obligatoire pour toute mission.  
  – Qui : Voyageur  
  – Validation : Superviseur  
  – Code : `TA-XXX-YY-001` (initiales–année–n°)  
  – Stockage : _Outlook / Public Folders / AV Logistics / Year / Flights / Staff ou Invitee_

- **Meeting Form (MF)**  
  Réunions avec plusieurs invités.  
  Remplace le TA pour participants extérieurs.

---

- **Vol** via NGO Travels (Genève), Aladin Voyages (Tunis)  
  TA validé → options → pré-réservation → confirmation → émission → billet  
  Tarifs ONG possibles (attestation KLM, AF…)

- **Classe**  
  • Éco : < 11 h  
  • Premium Éco : nuit > 6 h  
  • Business : direct > 9 h ou total > 11 h (COO) — _Suspendu_

- **Train**  
  < 6 h Europe → privilégié  
  > 3 h → 1ʳᵉ classe  
  Suisse → SwissPass

- **Hébergement**  
  3/4★ max (5★ sur autorisation COO)  
  HD paie chambre + petit-déj + taxes (extras sauf blanchisserie ≤ 20 CHF/2 nuits)  
  Stockage : Outlook / AV Logistics / Hotels

- **Visa**  
  Géré par le logisticien (ambassade, CIBT, e-visa)
        """)

    # Section 2
    with st.expander("2. PROCÉDURES ADMINISTRATIVES"):
        st.markdown("""
- **Justificatifs**  
  Contrats + PO (> 1 000 CHF) + factures + formulaire vendeur  
  PO : taux Oanda, 3 devis si > 10 000 CHF

- **Paiements**  
  • AirPlus / AIDA Card (vols, hôtels, événements)  
  • Virement bancaire (hebdo ; dépôt vendredi → paiement mercredi)  
  • Carte UBS (paiements directs, réconciliation fin de mois)  
  • Espèces (exceptionnel → liquidation avance)

- **EC / Note de frais**  
  Soumission dans 15 j avec originaux  
  DSA & frais selon TA  
  Taux Oanda (cash)  
  HD Receipt si reçu manquant + memo si perdu

- **Avance de caisse**  
  Demande → signature PM/DoF → liquidation via EC (montant négatif)
        """)

    # Section 3
    with st.expander("3. SÉCURITÉ DES MISSIONS"):
        st.markdown("""
- **Exiger** : Vérif. noms (sanctions) — rouge = alerte DED  
- **Docs avant mission à risque** : ToR + TA, Travel Release (1×/an), Proof of Life (1×/pays)  
- **Assurances**  
  • TSM (médical & évacuation)  
  • GardaWorld (pays à haut risque)  
  • Lloyd’s (assurance guerre → info CBI)
        """)

    # Section 4
    with st.expander("📂 FICHIERS UTILES"):
        st.markdown("""
- TA / MF / PO / EC / Approval stamp  
- Attestations ONG  
- Liste hôtels partenaires (5★ validé par Dalhia)  
- Relevés AirPlus / AIDA  
- Dossiers Outlook → AV Logistics (par type)
        """)

    st.markdown("---")
    st.caption("© HD Centre – MENA Logistics Procedures")
