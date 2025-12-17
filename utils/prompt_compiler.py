"""
Prompt compilation and validation utilities.

Handles variable substitution and validation for prompt templates.
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from html import escape


class ValidationError:
    """Represents a validation error."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

    def to_dict(self) -> Dict[str, str]:
        return {"field": self.field, "message": self.message}


class ValidationResult:
    """Result of template validation."""

    def __init__(self):
        self.is_valid = True
        self.errors: List[ValidationError] = []

    def add_error(self, field: str, message: str):
        """Add a validation error."""
        self.is_valid = False
        self.errors.append(ValidationError(field, message))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "isValid": self.is_valid,
            "errors": {e.field: e.message for e in self.errors}
        }


def extract_variables(template: str) -> List[str]:
    """
    Extract variable names from a template.

    Args:
        template: Template string with [variable_name] placeholders

    Returns:
        List of unique variable names found in template
    """
    pattern = r'\[(\w+)\]'
    matches = re.findall(pattern, template)
    # Return unique names while preserving order
    seen = set()
    result = []
    for name in matches:
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result


def compile_prompt(template: str, values: Dict[str, str]) -> str:
    """
    Compile a template by substituting variable values.

    Args:
        template: Template string with [variable_name] placeholders
        values: Dictionary of variable name -> value

    Returns:
        Compiled prompt with variables replaced
    """
    result = template

    for name, value in values.items():
        # Replace [variable_name] with the value
        pattern = r'\[' + re.escape(name) + r'\]'
        result = re.sub(pattern, value, result)

    return result


def validate_variable(
    variable_def: Dict[str, Any],
    value: str
) -> Optional[str]:
    """
    Validate a single variable value.

    Args:
        variable_def: Variable definition dictionary
        value: Value to validate

    Returns:
        Error message if invalid, None if valid
    """
    name = variable_def.get('name', 'field')
    required = variable_def.get('required', False)
    var_type = variable_def.get('type', 'text')
    validation = variable_def.get('validation', {})

    # Check required
    if required and not value.strip():
        return f"{variable_def.get('label', name)} is required"

    # Skip further validation if empty and not required
    if not value.strip():
        return None

    # Type-specific validation
    if var_type == 'url':
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, value, re.IGNORECASE):
            return validation.get('errorMessage', 'Please enter a valid URL')

    elif var_type == 'number':
        try:
            num = float(value)
            min_val = validation.get('min')
            max_val = validation.get('max')

            if min_val is not None and num < min_val:
                return validation.get('errorMessage', f'Value must be at least {min_val}')
            if max_val is not None and num > max_val:
                return validation.get('errorMessage', f'Value must be at most {max_val}')
        except ValueError:
            return validation.get('errorMessage', 'Please enter a valid number')

    elif var_type == 'date':
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, value):
            return validation.get('errorMessage', 'Please enter a valid date (YYYY-MM-DD)')

    # String validation
    if validation:
        pattern = validation.get('pattern')
        min_length = validation.get('minLength')
        max_length = validation.get('maxLength')

        if pattern:
            try:
                if not re.match(pattern, value):
                    return validation.get('errorMessage', f'Invalid format for {name}')
            except re.error:
                pass  # Invalid regex, skip validation

        if min_length is not None and len(value) < min_length:
            return validation.get('errorMessage', f'Must be at least {min_length} characters')

        if max_length is not None and len(value) > max_length:
            return validation.get('errorMessage', f'Must be at most {max_length} characters')

    return None


def validate_template_values(
    template_def: Dict[str, Any],
    values: Dict[str, str]
) -> ValidationResult:
    """
    Validate all variable values for a template.

    Args:
        template_def: Template definition dictionary
        values: Dictionary of variable name -> value

    Returns:
        ValidationResult with errors if any
    """
    result = ValidationResult()
    variables = template_def.get('variables', [])

    for variable in variables:
        name = variable.get('name')
        value = values.get(name, '')
        error = validate_variable(variable, value)

        if error:
            result.add_error(name, error)

    return result


def sanitize_value(value: str, var_type: str = 'text') -> str:
    """
    Sanitize a variable value for safe inclusion in prompt.

    Args:
        value: Raw value
        var_type: Variable type

    Returns:
        Sanitized value
    """
    if not value:
        return ''

    # Basic sanitization - remove control characters
    sanitized = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')

    # Trim excessive whitespace
    lines = sanitized.split('\n')
    lines = [' '.join(line.split()) for line in lines]
    sanitized = '\n'.join(lines)

    return sanitized.strip()


def get_unfilled_variables(template: str, values: Dict[str, str]) -> List[str]:
    """
    Get list of variables that haven't been filled in.

    Args:
        template: Template string
        values: Current values

    Returns:
        List of unfilled variable names
    """
    all_vars = extract_variables(template)
    unfilled = []

    for var in all_vars:
        if var not in values or not values[var].strip():
            unfilled.append(var)

    return unfilled


def estimate_token_count(text: str) -> int:
    """
    Estimate token count for a text string.

    Simple estimation: ~4 characters per token on average.

    Args:
        text: Text to estimate

    Returns:
        Estimated token count
    """
    return max(1, len(text) // 4)


def format_multiselect_value(values: List[str]) -> str:
    """
    Format multiselect values for display in prompt.

    Args:
        values: List of selected values

    Returns:
        Formatted string
    """
    if not values:
        return ''

    if len(values) == 1:
        return values[0]

    if len(values) == 2:
        return f"{values[0]} and {values[1]}"

    return ', '.join(values[:-1]) + f', and {values[-1]}'


def preview_compiled_prompt(
    template: str,
    values: Dict[str, str],
    highlight_unfilled: bool = True
) -> Dict[str, Any]:
    """
    Generate a preview of the compiled prompt.

    Args:
        template: Template string
        values: Variable values
        highlight_unfilled: Whether to mark unfilled variables

    Returns:
        Dictionary with preview info
    """
    compiled = compile_prompt(template, values)
    unfilled = get_unfilled_variables(template, values)

    return {
        "compiled": compiled,
        "unfilled": unfilled,
        "hasUnfilled": len(unfilled) > 0,
        "characterCount": len(compiled),
        "estimatedTokens": estimate_token_count(compiled)
    }
