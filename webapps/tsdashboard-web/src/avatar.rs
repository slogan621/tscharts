//! HTML helpers for patient headshot thumbnails (served via BFF proxy).

use crate::html::escape;

/// Size classes: `sm` (list), `md` (cards), `lg` (edit page).
pub fn headshot_img(patient_id: i64, size: &str, alt: &str) -> String {
    let cls = match size {
        "lg" => "avatar avatar-lg",
        "md" => "avatar avatar-md",
        _ => "avatar avatar-sm",
    };
    format!(
        r#"<img class="{cls}" src="/patients/{id}/headshot" alt="{alt}" loading="lazy" onerror="this.classList.add('missing');this.removeAttribute('src');">"#,
        cls = cls,
        id = patient_id,
        alt = escape(alt),
    )
}
