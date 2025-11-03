"""
Keyboard Shortcuts and Accessibility Support
Handles keyboard navigation and ARIA labels for WCAG 2.1 AA compliance
"""

import streamlit as st
from streamlit import session_state as ss


def setup_keyboard_shortcuts():
    """
    Setup keyboard shortcuts for Streamlit app
    Note: Streamlit has limited keyboard event support, so we use JavaScript
    """
    keyboard_script = """
    <script>
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter or Cmd+Enter to start research
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            // Find the start research button and click it
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent.includes('Start Research') || btn.textContent.includes('🚀')) {
                    e.preventDefault();
                    btn.click();
                    break;
                }
            }
        }
        
        // Ctrl+D or Cmd+D to download (when results are available)
        if ((e.ctrlKey || e.metaKey) && e.key === 'd' || e.key === 'D') {
            // Find download buttons
            const downloadButtons = document.querySelectorAll('a[download]');
            if (downloadButtons.length > 0) {
                e.preventDefault();
                // Trigger first available download (typically JSON)
                downloadButtons[0].click();
            }
        }
        
        // Tab navigation enhancement - ensure all interactive elements are focusable
        if (e.key === 'Tab') {
            // Ensure decision cards are keyboard accessible
            const decisionCards = document.querySelectorAll('.decision-card');
            decisionCards.forEach(card => {
                if (!card.hasAttribute('tabindex')) {
                    card.setAttribute('tabindex', '0');
                    card.setAttribute('role', 'button');
                    card.setAttribute('aria-label', 'Agent decision card');
                }
            });
        }
    });
    
    // Add ARIA labels to interactive elements
    window.addEventListener('load', function() {
        // Add ARIA labels to buttons
        document.querySelectorAll('button').forEach(btn => {
            if (!btn.hasAttribute('aria-label')) {
                const text = btn.textContent.trim();
                if (text) {
                    btn.setAttribute('aria-label', text);
                }
            }
        });
        
        // Add ARIA labels to download buttons
        document.querySelectorAll('a[download]').forEach(link => {
            if (!link.hasAttribute('aria-label')) {
                const text = link.textContent.trim() || 'Download';
                link.setAttribute('aria-label', `Download ${text}`);
            }
        });
        
        // Make decision cards keyboard accessible
        document.querySelectorAll('.decision-card').forEach(card => {
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'article');
            card.setAttribute('aria-label', 'Agent decision');
        });
        
        // Add ARIA labels to expanders
        document.querySelectorAll('[data-testid="stExpander"]').forEach(expander => {
            const header = expander.querySelector('[data-testid="stExpanderToggle"]');
            if (header && !header.hasAttribute('aria-label')) {
                const text = header.textContent.trim();
                header.setAttribute('aria-label', `Expand or collapse ${text}`);
            }
        });
    });
    </script>
    """
    st.markdown(keyboard_script, unsafe_allow_html=True)


def add_aria_labels_to_decision_card(agent: str, decision_type: str, decision: str) -> str:
    """Generate ARIA-friendly attributes for decision cards"""
    return f"""
    role="article"
    aria-label="{agent} decision: {decision_type}"
    aria-describedby="decision-{agent}-{decision_type}"
    tabindex="0"
    """

