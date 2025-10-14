API_KEY = ""
API_ENDPOINT = ("https://els-openai-hackathon-1065.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api"
                "-version=2025-01-01-preview")
CERT_PATH = "/etc/ssl/cert.pem"
MODEL_NAME = "gpt-4.1"

USER_PROFILES = {
    "product": "Focus on product features, roadmap, customer value.",
    "quality": "Focus on testing, defects, quality metrics, improvements.",
    "project": "Focus on timelines, milestones, deliverables, blockers.",
    "customer": "Focus on customer needs, feedback, satisfaction.",
    "engineering": "Focus on technical challenges, solutions, architecture.",
    "project_management": "Focus on planning, risks, resources, coordination.",
    "new_joinee_or_onboarding": "Focus on onboarding, orientation, and learning resources for new joiners."
}