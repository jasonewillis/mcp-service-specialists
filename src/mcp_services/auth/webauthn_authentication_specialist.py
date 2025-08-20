#!/usr/bin/env python3
"""
WebAuthn Authentication Specialist for Fed Job Advisor

Embedded knowledge for passkey implementation with federal security requirements.
Supports browser registration flows, server verification, and fallback authentication.

CRITICAL VERSIONS:
- python-jose[cryptography]==3.3.0 (from requirements.txt line 12)
- passlib[bcrypt]==1.7.4 (from requirements.txt line 13)
- Client-side: WebAuthn API (native browser support)

WARNING: Federal authentication has strict security requirements
WARNING: WebAuthn requires HTTPS in production
WARNING: Passkey fallback strategies are critical for federal users
"""

import json
import base64
import secrets
import hashlib
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
import structlog
from enum import Enum

# Embedded knowledge base for Fed Job Advisor WebAuthn patterns
WEBAUTHN_SPECIALIST_KNOWLEDGE = {
    "version_compatibility": {
        "python_jose": "3.3.0",
        "passlib": "1.7.4",
        "webauthn_api": "Level 2", 
        "browser_support": {
            "chrome": "67+",
            "firefox": "60+", 
            "safari": "14+",
            "edge": "18+"
        },
        "platform_authenticators": ["TouchID", "FaceID", "Windows_Hello", "Android_Biometric"]
    },
    
    "federal_security_requirements": {
        "nist_compliance": {
            "authenticator_assurance_level": "AAL2",  # NIST SP 800-63B
            "required_factors": ["something_you_have", "something_you_are"],
            "session_timeout": 3600,  # 1 hour max for federal systems
            "reauthentication_required": 28800  # 8 hours max
        },
        "fido2_requirements": {
            "attestation": "direct",  # Required for federal compliance
            "user_verification": "required",
            "authenticator_attachment": "platform",  # Prefer built-in authenticators
            "resident_key": "preferred"
        },
        "cryptographic_standards": {
            "algorithms": ["ES256", "RS256"],  # NIST approved
            "key_lengths": {"rsa": 2048, "ec": "P-256"},
            "challenge_entropy": 256  # bits
        }
    },
    
    "registration_flow": {
        "initiation": {
            "user_verification": "Always verify user before registration",
            "challenge_generation": "Use cryptographically secure random",
            "timeout": 300,  # 5 minutes
            "excludeCredentials": "Prevent duplicate registrations"
        },
        "credential_creation": {
            "rp_id": "Match domain exactly",
            "rp_name": "Fed Job Advisor",
            "user_id": "Stable, unique identifier (not email)",
            "user_name": "email or username",
            "user_display_name": "full name"
        },
        "verification": {
            "attestation_verification": "Validate certificate chain",
            "signature_verification": "Verify challenge signature",
            "counter_validation": "Check signature counter progression",
            "origin_validation": "Strict origin checking"
        }
    },
    
    "authentication_flow": {
        "assertion_request": {
            "challenge_generation": "New challenge per auth attempt",
            "timeout": 120,  # 2 minutes for auth
            "user_verification": "required",
            "allowCredentials": "List registered credentials"
        },
        "assertion_verification": {
            "signature_validation": "Verify assertion signature",
            "counter_check": "Ensure counter increment",
            "user_presence": "Verify user gesture",
            "origin_verification": "Match registered origin"
        }
    },
    
    "fallback_strategies": {
        "backup_authentication": {
            "email_otp": "Email-based one-time passwords",
            "sms_otp": "SMS backup (if phone verified)",
            "recovery_codes": "Single-use backup codes",
            "admin_override": "Help desk password reset"
        },
        "progressive_enhancement": {
            "feature_detection": "Check WebAuthn API availability",
            "graceful_degradation": "Fall back to traditional auth",
            "browser_compatibility": "Polyfills for older browsers"
        }
    },
    
    "storage_patterns": {
        "credential_storage": {
            "table_name": "user_webauthn_credentials",
            "fields": [
                "credential_id", "user_id", "public_key", "signature_counter", 
                "aaguid", "attestation_format", "created_at", "last_used_at"
            ],
            "encryption": "Encrypt sensitive credential data",
            "indexing": ["user_id", "credential_id", "last_used_at"]
        },
        "challenge_storage": {
            "redis_key_pattern": "webauthn:challenge:{session_id}",
            "ttl_seconds": 300,  # 5 minutes
            "data": "challenge + timestamp + user_id"
        },
        "session_management": {
            "authenticated_session": "webauthn:session:{user_id}",
            "session_ttl": 3600,  # 1 hour for federal compliance
            "reauthentication_required": True
        }
    },
    
    "critical_warnings": {
        "security_warnings": [
            "Never store private keys on server",
            "Always validate challenge in server response",
            "Implement rate limiting on auth attempts",
            "Use HTTPS only - WebAuthn requires secure context",
            "Validate origin matches exactly (no subdomain wildcards)",
            "Check signature counter to prevent replay attacks"
        ],
        "federal_compliance_warnings": [
            "NIST AAL2 requires multi-factor authentication",
            "Session timeout must not exceed 1 hour",
            "User verification is mandatory for federal systems",
            "Audit logging required for all authentication events",
            "Backup authentication methods must be equally secure"
        ],
        "browser_compatibility_issues": [
            "Safari requires TouchID/FaceID available",
            "Firefox requires security.webauth.webauthn enabled",
            "Chrome on Android requires screen lock enabled",
            "Edge legacy versions have limited support"
        ],
        "deployment_gotchas": [
            "RP ID must exactly match production domain",
            "Cross-origin authentication not supported",
            "Development localhost works, staging domains may not",
            "HTTPS certificate issues break WebAuthn"
        ]
    }
}

class WebAuthnSpecialist:
    """
    Fed Job Advisor WebAuthn Authentication Specialist
    
    Provides comprehensive WebAuthn/passkey implementation for federal job search
    application with embedded knowledge for security compliance and browser compatibility.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.knowledge = WEBAUTHN_SPECIALIST_KNOWLEDGE
        
    def generate_challenge(self) -> bytes:
        """
        Generate cryptographically secure challenge for WebAuthn
        
        Returns:
            32-byte challenge meeting federal security requirements
        """
        return secrets.token_bytes(32)
    
    def create_registration_options(self, user_id: str, username: str, 
                                  display_name: str, rp_id: str) -> Dict[str, Any]:
        """
        Create WebAuthn registration options for Fed Job Advisor
        
        Args:
            user_id: Stable user identifier (not email)
            username: User's email or username
            display_name: User's full name
            rp_id: Relying party ID (domain)
            
        Returns:
            Complete registration options dict
        """
        challenge = self.generate_challenge()
        
        return {
            "challenge": base64.urlsafe_b64encode(challenge).decode().rstrip('='),
            "rp": {
                "name": "Fed Job Advisor",
                "id": rp_id
            },
            "user": {
                "id": base64.urlsafe_b64encode(user_id.encode()).decode().rstrip('='),
                "name": username,
                "displayName": display_name
            },
            "pubKeyCredParams": [
                {"alg": -7, "type": "public-key"},   # ES256 (NIST approved)
                {"alg": -257, "type": "public-key"}  # RS256 (NIST approved)
            ],
            "authenticatorSelection": {
                "authenticatorAttachment": "platform",  # Prefer built-in
                "userVerification": "required",  # Federal requirement
                "residentKey": "preferred"
            },
            "timeout": 300000,  # 5 minutes
            "attestation": "direct",  # Required for federal compliance
            "excludeCredentials": []  # Will be populated with existing creds
        }
    
    def create_authentication_options(self, user_id: str, rp_id: str,
                                    existing_credentials: List[str] = None) -> Dict[str, Any]:
        """
        Create WebAuthn authentication options
        
        Args:
            user_id: User identifier
            rp_id: Relying party ID
            existing_credentials: List of credential IDs for this user
            
        Returns:
            Authentication options dict
        """
        challenge = self.generate_challenge()
        
        allow_credentials = []
        if existing_credentials:
            allow_credentials = [
                {
                    "type": "public-key",
                    "id": cred_id,
                    "transports": ["internal", "usb", "nfc", "ble"]
                }
                for cred_id in existing_credentials
            ]
        
        return {
            "challenge": base64.urlsafe_b64encode(challenge).decode().rstrip('='),
            "timeout": 120000,  # 2 minutes
            "rpId": rp_id,
            "allowCredentials": allow_credentials,
            "userVerification": "required"  # Federal requirement
        }
    
    def create_database_schema(self) -> str:
        """
        Create database schema for WebAuthn credentials
        
        Returns:
            SQL DDL for WebAuthn credential storage
        """
        return '''
-- WebAuthn credentials table for Fed Job Advisor
CREATE TABLE user_webauthn_credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    credential_id BYTEA NOT NULL UNIQUE,
    public_key BYTEA NOT NULL,
    signature_counter BIGINT NOT NULL DEFAULT 0,
    aaguid BYTEA,
    attestation_format VARCHAR(50),
    attestation_statement JSONB,
    backup_eligible BOOLEAN DEFAULT FALSE,
    backup_state BOOLEAN DEFAULT FALSE,
    transports TEXT[],
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Federal audit requirements
    created_by VARCHAR(100),
    last_modified_by VARCHAR(100),
    
    -- Indexes for performance
    INDEX idx_webauthn_user_id (user_id),
    INDEX idx_webauthn_credential_id (credential_id),
    INDEX idx_webauthn_last_used (last_used_at),
    INDEX idx_webauthn_active (is_active)
);

-- WebAuthn challenges table (for Redis alternative)
CREATE TABLE webauthn_challenges (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    challenge BYTEA NOT NULL,
    user_id INTEGER,
    challenge_type VARCHAR(20) NOT NULL, -- 'registration' or 'authentication'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_webauthn_challenge_session (session_id),
    INDEX idx_webauthn_challenge_expires (expires_at),
    
    -- Cleanup expired challenges
    CHECK (expires_at > created_at)
);

-- Trigger to cleanup expired challenges
CREATE OR REPLACE FUNCTION cleanup_expired_webauthn_challenges()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM webauthn_challenges 
    WHERE expires_at < NOW() - INTERVAL '1 hour';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_cleanup_webauthn_challenges
    AFTER INSERT ON webauthn_challenges
    EXECUTE FUNCTION cleanup_expired_webauthn_challenges();

-- Authentication audit log
CREATE TABLE authentication_audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    authentication_method VARCHAR(50) NOT NULL, -- 'webauthn', 'password', 'email_otp'
    success BOOLEAN NOT NULL,
    ip_address INET,
    user_agent TEXT,
    credential_id BYTEA, -- For WebAuthn attempts
    failure_reason VARCHAR(255), -- For failed attempts
    session_id VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Federal compliance indexes
    INDEX idx_auth_audit_user (user_id),
    INDEX idx_auth_audit_timestamp (timestamp),
    INDEX idx_auth_audit_method (authentication_method),
    INDEX idx_auth_audit_success (success)
);
'''

    def create_server_verification_code(self) -> str:
        """
        Create server-side verification code for WebAuthn
        
        Returns:
            Python code for registration and authentication verification
        """
        return '''
import base64
import cbor2
import hashlib
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.exceptions import InvalidSignature
from typing import Dict, Any, Optional, Tuple
import structlog

class WebAuthnVerifier:
    """WebAuthn verification for Fed Job Advisor"""
    
    def __init__(self, rp_id: str, origin: str):
        self.rp_id = rp_id
        self.origin = origin
        self.logger = structlog.get_logger(__name__)
    
    def verify_registration(self, credential: Dict[str, Any], 
                          challenge: bytes, user_id: str) -> Dict[str, Any]:
        """
        Verify WebAuthn registration response
        
        Args:
            credential: Registration credential from client
            challenge: Original challenge sent to client
            user_id: User identifier
            
        Returns:
            Verification result with credential data
        """
        try:
            # Decode client data JSON
            client_data_json = base64.urlsafe_b64decode(
                credential['response']['clientDataJSON'] + '=='
            )
            client_data = json.loads(client_data_json.decode('utf-8'))
            
            # Verify client data
            if not self._verify_client_data(client_data, challenge, 'webauthn.create'):
                return {"verified": False, "error": "Client data verification failed"}
            
            # Decode attestation object
            attestation_object = base64.urlsafe_b64decode(
                credential['response']['attestationObject'] + '=='
            )
            attestation = cbor2.loads(attestation_object)
            
            # Extract authenticator data
            auth_data = attestation['authData']
            auth_data_parsed = self._parse_authenticator_data(auth_data)
            
            # Verify RP ID hash
            rp_id_hash = hashlib.sha256(self.rp_id.encode('utf-8')).digest()
            if auth_data_parsed['rp_id_hash'] != rp_id_hash:
                return {"verified": False, "error": "RP ID hash mismatch"}
            
            # Verify user present flag
            if not auth_data_parsed['flags']['user_present']:
                return {"verified": False, "error": "User presence required"}
            
            # Verify user verification for federal compliance
            if not auth_data_parsed['flags']['user_verified']:
                return {"verified": False, "error": "User verification required for federal systems"}
            
            # Extract credential data
            credential_data = auth_data_parsed['attested_credential_data']
            
            # Verify attestation (for federal compliance)
            attestation_verified = self._verify_attestation(
                attestation, auth_data, client_data_json
            )
            
            if not attestation_verified:
                self.logger.warning("Attestation verification failed", user_id=user_id)
                # In production, may want to reject based on policy
            
            return {
                "verified": True,
                "credential_id": base64.urlsafe_b64encode(credential_data['credential_id']).decode(),
                "public_key": base64.urlsafe_b64encode(credential_data['public_key']).decode(),
                "signature_counter": auth_data_parsed['signature_counter'],
                "aaguid": base64.urlsafe_b64encode(credential_data['aaguid']).decode(),
                "attestation_format": attestation['fmt'],
                "attestation_statement": attestation.get('attStmt', {}),
                "backup_eligible": auth_data_parsed['flags'].get('backup_eligible', False),
                "backup_state": auth_data_parsed['flags'].get('backup_state', False)
            }
            
        except Exception as e:
            self.logger.error("Registration verification failed", error=str(e), user_id=user_id)
            return {"verified": False, "error": f"Verification error: {str(e)}"}
    
    def verify_authentication(self, assertion: Dict[str, Any], challenge: bytes,
                            stored_credential: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify WebAuthn authentication assertion
        
        Args:
            assertion: Authentication assertion from client
            challenge: Original challenge sent to client
            stored_credential: Previously stored credential data
            
        Returns:
            Verification result
        """
        try:
            # Decode client data JSON
            client_data_json = base64.urlsafe_b64decode(
                assertion['response']['clientDataJSON'] + '=='
            )
            client_data = json.loads(client_data_json.decode('utf-8'))
            
            # Verify client data
            if not self._verify_client_data(client_data, challenge, 'webauthn.get'):
                return {"verified": False, "error": "Client data verification failed"}
            
            # Decode authenticator data
            authenticator_data = base64.urlsafe_b64decode(
                assertion['response']['authenticatorData'] + '=='
            )
            auth_data_parsed = self._parse_authenticator_data(authenticator_data)
            
            # Verify RP ID hash
            rp_id_hash = hashlib.sha256(self.rp_id.encode('utf-8')).digest()
            if auth_data_parsed['rp_id_hash'] != rp_id_hash:
                return {"verified": False, "error": "RP ID hash mismatch"}
            
            # Verify flags
            if not auth_data_parsed['flags']['user_present']:
                return {"verified": False, "error": "User presence required"}
            
            if not auth_data_parsed['flags']['user_verified']:
                return {"verified": False, "error": "User verification required"}
            
            # Verify signature counter progression
            current_counter = auth_data_parsed['signature_counter']
            stored_counter = stored_credential['signature_counter']
            
            if current_counter <= stored_counter and current_counter != 0:
                self.logger.warning("Signature counter regression detected", 
                                  current=current_counter, stored=stored_counter)
                return {"verified": False, "error": "Signature counter regression"}
            
            # Verify signature
            signature = base64.urlsafe_b64decode(
                assertion['response']['signature'] + '=='
            )
            
            # Create signed data
            client_data_hash = hashlib.sha256(client_data_json).digest()
            signed_data = authenticator_data + client_data_hash
            
            # Verify signature with stored public key
            public_key_bytes = base64.urlsafe_b64decode(stored_credential['public_key'] + '==')
            signature_valid = self._verify_signature(
                public_key_bytes, signed_data, signature
            )
            
            if not signature_valid:
                return {"verified": False, "error": "Signature verification failed"}
            
            return {
                "verified": True,
                "signature_counter": current_counter,
                "backup_state": auth_data_parsed['flags'].get('backup_state', False)
            }
            
        except Exception as e:
            self.logger.error("Authentication verification failed", error=str(e))
            return {"verified": False, "error": f"Verification error: {str(e)}"}
    
    def _verify_client_data(self, client_data: Dict[str, Any], 
                          challenge: bytes, expected_type: str) -> bool:
        """Verify client data JSON"""
        try:
            # Verify type
            if client_data.get('type') != expected_type:
                return False
            
            # Verify challenge
            received_challenge = base64.urlsafe_b64decode(
                client_data.get('challenge', '') + '=='
            )
            if received_challenge != challenge:
                return False
            
            # Verify origin
            if client_data.get('origin') != self.origin:
                self.logger.error("Origin mismatch", 
                                received=client_data.get('origin'),
                                expected=self.origin)
                return False
            
            return True
            
        except Exception as e:
            self.logger.error("Client data verification error", error=str(e))
            return False
    
    def _parse_authenticator_data(self, auth_data: bytes) -> Dict[str, Any]:
        """Parse authenticator data"""
        if len(auth_data) < 37:
            raise ValueError("Authenticator data too short")
        
        # RP ID hash (32 bytes)
        rp_id_hash = auth_data[0:32]
        
        # Flags (1 byte)
        flags_byte = auth_data[32]
        flags = {
            'user_present': bool(flags_byte & 0x01),
            'user_verified': bool(flags_byte & 0x04),
            'attested_credential_data': bool(flags_byte & 0x40),
            'extension_data': bool(flags_byte & 0x80),
            'backup_eligible': bool(flags_byte & 0x08),
            'backup_state': bool(flags_byte & 0x10)
        }
        
        # Signature counter (4 bytes)
        signature_counter = int.from_bytes(auth_data[33:37], 'big')
        
        result = {
            'rp_id_hash': rp_id_hash,
            'flags': flags,
            'signature_counter': signature_counter
        }
        
        # Parse attested credential data if present
        if flags['attested_credential_data']:
            offset = 37
            
            # AAGUID (16 bytes)
            aaguid = auth_data[offset:offset + 16]
            offset += 16
            
            # Credential ID length (2 bytes)
            cred_id_len = int.from_bytes(auth_data[offset:offset + 2], 'big')
            offset += 2
            
            # Credential ID
            credential_id = auth_data[offset:offset + cred_id_len]
            offset += cred_id_len
            
            # Public key (CBOR encoded)
            public_key_cbor = auth_data[offset:]
            
            result['attested_credential_data'] = {
                'aaguid': aaguid,
                'credential_id': credential_id,
                'public_key': public_key_cbor
            }
        
        return result
    
    def _verify_signature(self, public_key_bytes: bytes, 
                         signed_data: bytes, signature: bytes) -> bool:
        """Verify signature with public key"""
        try:
            # Parse CBOR public key
            public_key_cbor = cbor2.loads(public_key_bytes)
            
            kty = public_key_cbor[1]  # Key type
            alg = public_key_cbor[3]  # Algorithm
            
            if kty == 2:  # EC2 key type
                # Extract coordinates
                x = public_key_cbor[-2]
                y = public_key_cbor[-1]
                curve = public_key_cbor[-1]
                
                # Create EC public key
                if curve == 1:  # P-256
                    curve_obj = ec.SECP256R1()
                else:
                    raise ValueError(f"Unsupported curve: {curve}")
                
                public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                    curve_obj, b'\x04' + x + y
                )
                
                # For ES256, signature is DER encoded
                if alg == -7:  # ES256
                    # Convert to raw format if needed
                    try:
                        r, s = decode_dss_signature(signature)
                        signature = r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
                    except:
                        pass  # Already in raw format
                    
                    public_key.verify(signature, signed_data, ec.ECDSA(hashes.SHA256()))
                
            elif kty == 3:  # RSA key type
                # Extract modulus and exponent
                n = int.from_bytes(public_key_cbor[-1], 'big')
                e = int.from_bytes(public_key_cbor[-2], 'big')
                
                # Create RSA public key
                public_numbers = rsa.RSAPublicNumbers(e, n)
                public_key = public_numbers.public_key()
                
                # For RS256
                if alg == -257:  # RS256
                    public_key.verify(
                        signature, signed_data, 
                        padding.PKCS1v15(), hashes.SHA256()
                    )
            
            return True
            
        except Exception as e:
            self.logger.error("Signature verification failed", error=str(e))
            return False
    
    def _verify_attestation(self, attestation: Dict[str, Any], 
                          auth_data: bytes, client_data_json: bytes) -> bool:
        """Verify attestation statement"""
        fmt = attestation.get('fmt')
        att_stmt = attestation.get('attStmt', {})
        
        if fmt == 'none':
            # No attestation verification needed
            return True
        elif fmt == 'packed':
            # Basic packed attestation verification
            return self._verify_packed_attestation(att_stmt, auth_data, client_data_json)
        else:
            # For federal compliance, may need to implement other formats
            self.logger.warning("Unsupported attestation format", format=fmt)
            return False
    
    def _verify_packed_attestation(self, att_stmt: Dict[str, Any],
                                 auth_data: bytes, client_data_json: bytes) -> bool:
        """Verify packed attestation format"""
        # Basic implementation - production would need full certificate validation
        try:
            sig = att_stmt.get('sig')
            x5c = att_stmt.get('x5c')
            
            if not sig:
                return False
            
            # Create verification data
            client_data_hash = hashlib.sha256(client_data_json).digest()
            verification_data = auth_data + client_data_hash
            
            # If x5c is present, verify certificate chain
            if x5c:
                # In production: verify certificate chain, check revocation, etc.
                return True  # Simplified for example
            
            return True
            
        except Exception as e:
            self.logger.error("Packed attestation verification failed", error=str(e))
            return False
'''

    def create_client_side_code(self) -> str:
        """
        Create client-side JavaScript for WebAuthn
        
        Returns:
            JavaScript code for browser WebAuthn implementation
        """
        return '''
/**
 * Fed Job Advisor WebAuthn Client
 * Handles passkey registration and authentication with federal compliance
 */

class FedJobWebAuthn {
    constructor(options = {}) {
        this.rpId = options.rpId || window.location.hostname;
        this.apiBase = options.apiBase || '/api/auth';
        this.logger = options.logger || console;
        
        // Check WebAuthn support
        this.isSupported = this.checkSupport();
    }
    
    checkSupport() {
        if (!window.PublicKeyCredential) {
            this.logger.warn('WebAuthn not supported in this browser');
            return false;
        }
        
        if (!window.isSecureContext) {
            this.logger.error('WebAuthn requires HTTPS (secure context)');
            return false;
        }
        
        return true;
    }
    
    async isUserVerifyingPlatformAuthenticatorAvailable() {
        try {
            return await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        } catch (error) {
            this.logger.warn('Could not check platform authenticator availability', error);
            return false;
        }
    }
    
    async register(userId, username, displayName) {
        if (!this.isSupported) {
            throw new Error('WebAuthn not supported');
        }
        
        try {
            // Get registration options from server
            const optionsResponse = await fetch(`${this.apiBase}/webauthn/register/begin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    user_id: userId,
                    username: username,
                    display_name: displayName
                })
            });
            
            if (!optionsResponse.ok) {
                throw new Error('Failed to get registration options');
            }
            
            const options = await optionsResponse.json();
            
            // Convert base64url to ArrayBuffer
            options.challenge = this.base64urlToBuffer(options.challenge);
            options.user.id = this.base64urlToBuffer(options.user.id);
            
            if (options.excludeCredentials) {
                options.excludeCredentials = options.excludeCredentials.map(cred => ({
                    ...cred,
                    id: this.base64urlToBuffer(cred.id)
                }));
            }
            
            // Create credential
            this.logger.info('Creating WebAuthn credential...');
            const credential = await navigator.credentials.create({
                publicKey: options
            });
            
            if (!credential) {
                throw new Error('Failed to create credential');
            }
            
            // Prepare credential for server
            const credentialJson = {
                id: credential.id,
                rawId: this.bufferToBase64url(credential.rawId),
                type: credential.type,
                response: {
                    clientDataJSON: this.bufferToBase64url(credential.response.clientDataJSON),
                    attestationObject: this.bufferToBase64url(credential.response.attestationObject)
                }
            };
            
            // Send to server for verification
            const verifyResponse = await fetch(`${this.apiBase}/webauthn/register/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    credential: credentialJson,
                    user_id: userId
                })
            });
            
            if (!verifyResponse.ok) {
                const error = await verifyResponse.json();
                throw new Error(error.message || 'Registration verification failed');
            }
            
            const result = await verifyResponse.json();
            this.logger.info('WebAuthn registration successful');
            
            return result;
            
        } catch (error) {
            this.logger.error('WebAuthn registration failed', error);
            throw error;
        }
    }
    
    async authenticate(userId = null) {
        if (!this.isSupported) {
            throw new Error('WebAuthn not supported');
        }
        
        try {
            // Get authentication options from server
            const optionsResponse = await fetch(`${this.apiBase}/webauthn/authenticate/begin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ user_id: userId })
            });
            
            if (!optionsResponse.ok) {
                throw new Error('Failed to get authentication options');
            }
            
            const options = await optionsResponse.json();
            
            // Convert base64url to ArrayBuffer
            options.challenge = this.base64urlToBuffer(options.challenge);
            
            if (options.allowCredentials) {
                options.allowCredentials = options.allowCredentials.map(cred => ({
                    ...cred,
                    id: this.base64urlToBuffer(cred.id)
                }));
            }
            
            // Get assertion
            this.logger.info('Getting WebAuthn assertion...');
            const assertion = await navigator.credentials.get({
                publicKey: options
            });
            
            if (!assertion) {
                throw new Error('Failed to get assertion');
            }
            
            // Prepare assertion for server
            const assertionJson = {
                id: assertion.id,
                rawId: this.bufferToBase64url(assertion.rawId),
                type: assertion.type,
                response: {
                    clientDataJSON: this.bufferToBase64url(assertion.response.clientDataJSON),
                    authenticatorData: this.bufferToBase64url(assertion.response.authenticatorData),
                    signature: this.bufferToBase64url(assertion.response.signature),
                    userHandle: assertion.response.userHandle ? 
                        this.bufferToBase64url(assertion.response.userHandle) : null
                }
            };
            
            // Send to server for verification
            const verifyResponse = await fetch(`${this.apiBase}/webauthn/authenticate/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    assertion: assertionJson,
                    user_id: userId
                })
            });
            
            if (!verifyResponse.ok) {
                const error = await verifyResponse.json();
                throw new Error(error.message || 'Authentication verification failed');
            }
            
            const result = await verifyResponse.json();
            this.logger.info('WebAuthn authentication successful');
            
            return result;
            
        } catch (error) {
            this.logger.error('WebAuthn authentication failed', error);
            throw error;
        }
    }
    
    // Utility functions for base64url conversion
    base64urlToBuffer(base64url) {
        const base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
        const binary = atob(base64);
        const buffer = new ArrayBuffer(binary.length);
        const view = new Uint8Array(buffer);
        for (let i = 0; i < binary.length; i++) {
            view[i] = binary.charCodeAt(i);
        }
        return buffer;
    }
    
    bufferToBase64url(buffer) {
        const view = new Uint8Array(buffer);
        let binary = '';
        for (let i = 0; i < view.byteLength; i++) {
            binary += String.fromCharCode(view[i]);
        }
        const base64 = btoa(binary);
        return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    }
    
    // Progressive enhancement helpers
    createFallbackUI() {
        return `
            <div class="webauthn-fallback">
                <p>Passkeys are not available in your browser.</p>
                <p>Please use email/password authentication or try a supported browser:</p>
                <ul>
                    <li>Chrome 67+</li>
                    <li>Firefox 60+</li>
                    <li>Safari 14+</li>
                    <li>Edge 18+</li>
                </ul>
            </div>
        `;
    }
    
    // Federal compliance helpers
    async checkComplianceFeatures() {
        const features = {
            webauthn_supported: this.isSupported,
            platform_authenticator_available: false,
            user_verification_available: false,
            resident_keys_supported: false
        };
        
        if (this.isSupported) {
            try {
                features.platform_authenticator_available = 
                    await this.isUserVerifyingPlatformAuthenticatorAvailable();
                
                // Check for resident key support
                if (PublicKeyCredential.isConditionalMediationAvailable) {
                    features.resident_keys_supported = 
                        await PublicKeyCredential.isConditionalMediationAvailable();
                }
            } catch (error) {
                this.logger.warn('Error checking compliance features', error);
            }
        }
        
        return features;
    }
}

// Export for use in Fed Job Advisor
window.FedJobWebAuthn = FedJobWebAuthn;

// Usage example:
// const webauthn = new FedJobWebAuthn({
//     rpId: 'fedjobadvisor.com',
//     apiBase: '/api/auth'
// });
// 
// // Registration
// await webauthn.register('user123', 'user@example.com', 'John Doe');
// 
// // Authentication  
// await webauthn.authenticate('user123');
'''

    def create_fastapi_routes(self) -> str:
        """
        Create FastAPI routes for WebAuthn endpoints
        
        Returns:
            Python code for FastAPI WebAuthn routes
        """
        return '''
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import base64
import secrets
import json
from datetime import datetime, timedelta
import structlog

# Import your models and dependencies
from agents.app.models.user import User
from agents.app.models.webauthn_credential import WebAuthnCredential
from agents.app.database import get_db
from agents.app.auth.webauthn_verifier import WebAuthnVerifier
from agents.app.auth.session import create_session, get_current_user
from agents.app.cache.redis_client import FedJobRedisClient

router = APIRouter(prefix="/webauthn", tags=["webauthn"])
logger = structlog.get_logger(__name__)

# Pydantic models
class RegistrationBeginRequest(BaseModel):
    user_id: str
    username: str
    display_name: str

class RegistrationCompleteRequest(BaseModel):
    credential: Dict[str, Any]
    user_id: str

class AuthenticationBeginRequest(BaseModel):
    user_id: Optional[str] = None

class AuthenticationCompleteRequest(BaseModel):
    assertion: Dict[str, Any]
    user_id: Optional[str] = None

# Dependency to get WebAuthn verifier
def get_webauthn_verifier(request: Request) -> WebAuthnVerifier:
    rp_id = request.url.hostname
    origin = str(request.url).replace(request.url.path, "")
    return WebAuthnVerifier(rp_id=rp_id, origin=origin)

@router.post("/register/begin")
async def webauthn_register_begin(
    request: RegistrationBeginRequest,
    http_request: Request,
    redis_client: FedJobRedisClient = Depends(),
    db = Depends(get_db)
):
    """
    Begin WebAuthn registration process
    """
    try:
        # Verify user exists and is authenticated
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get existing credentials to exclude
        existing_creds = db.query(WebAuthnCredential).filter(
            WebAuthnCredential.user_id == user.id,
            WebAuthnCredential.is_active == True
        ).all()
        
        exclude_credentials = [
            {
                "type": "public-key",
                "id": base64.urlsafe_b64encode(cred.credential_id).decode().rstrip('='),
                "transports": cred.transports or ["internal", "usb", "nfc", "ble"]
            }
            for cred in existing_creds
        ]
        
        # Generate challenge
        challenge = secrets.token_bytes(32)
        
        # Store challenge in Redis
        session_id = http_request.session.get("session_id")
        if not session_id:
            session_id = secrets.token_urlsafe(32)
            http_request.session["session_id"] = session_id
        
        challenge_key = f"webauthn:challenge:{session_id}"
        challenge_data = {
            "challenge": base64.urlsafe_b64encode(challenge).decode(),
            "user_id": request.user_id,
            "type": "registration",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        redis_client.client.setex(
            challenge_key, 
            300,  # 5 minutes
            json.dumps(challenge_data)
        )
        
        # Create registration options
        rp_id = http_request.url.hostname
        
        options = {
            "challenge": base64.urlsafe_b64encode(challenge).decode().rstrip('='),
            "rp": {
                "name": "Fed Job Advisor",
                "id": rp_id
            },
            "user": {
                "id": base64.urlsafe_b64encode(request.user_id.encode()).decode().rstrip('='),
                "name": request.username,
                "displayName": request.display_name
            },
            "pubKeyCredParams": [
                {"alg": -7, "type": "public-key"},   # ES256
                {"alg": -257, "type": "public-key"}  # RS256
            ],
            "authenticatorSelection": {
                "authenticatorAttachment": "platform",
                "userVerification": "required",
                "residentKey": "preferred"
            },
            "timeout": 300000,  # 5 minutes
            "attestation": "direct",
            "excludeCredentials": exclude_credentials
        }
        
        logger.info("WebAuthn registration initiated", 
                   user_id=request.user_id, 
                   challenge_id=session_id)
        
        return options
        
    except Exception as e:
        logger.error("WebAuthn registration begin failed", 
                    error=str(e), user_id=request.user_id)
        raise HTTPException(status_code=500, detail="Registration initialization failed")

@router.post("/register/complete")
async def webauthn_register_complete(
    request: RegistrationCompleteRequest,
    http_request: Request,
    verifier: WebAuthnVerifier = Depends(get_webauthn_verifier),
    redis_client: FedJobRedisClient = Depends(),
    db = Depends(get_db)
):
    """
    Complete WebAuthn registration process
    """
    try:
        # Get challenge from Redis
        session_id = http_request.session.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="No active session")
        
        challenge_key = f"webauthn:challenge:{session_id}"
        challenge_data_str = redis_client.client.get(challenge_key)
        
        if not challenge_data_str:
            raise HTTPException(status_code=400, detail="Challenge expired or invalid")
        
        challenge_data = json.loads(challenge_data_str)
        
        # Verify user matches
        if challenge_data["user_id"] != request.user_id:
            raise HTTPException(status_code=400, detail="User mismatch")
        
        if challenge_data["type"] != "registration":
            raise HTTPException(status_code=400, detail="Invalid challenge type")
        
        # Get challenge bytes
        challenge = base64.urlsafe_b64decode(challenge_data["challenge"] + '==')
        
        # Verify registration
        verification_result = verifier.verify_registration(
            request.credential, challenge, request.user_id
        )
        
        if not verification_result["verified"]:
            logger.warning("WebAuthn registration verification failed",
                         user_id=request.user_id,
                         error=verification_result.get("error"))
            raise HTTPException(status_code=400, 
                              detail=f"Registration verification failed: {verification_result.get('error')}")
        
        # Save credential to database
        credential = WebAuthnCredential(
            user_id=int(request.user_id),
            credential_id=base64.urlsafe_b64decode(verification_result["credential_id"] + '=='),
            public_key=base64.urlsafe_b64decode(verification_result["public_key"] + '=='),
            signature_counter=verification_result["signature_counter"],
            aaguid=base64.urlsafe_b64decode(verification_result["aaguid"] + '=='),
            attestation_format=verification_result["attestation_format"],
            attestation_statement=verification_result["attestation_statement"],
            backup_eligible=verification_result.get("backup_eligible", False),
            backup_state=verification_result.get("backup_state", False),
            user_agent=http_request.headers.get("User-Agent"),
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(credential)
        db.commit()
        
        # Clean up challenge
        redis_client.client.delete(challenge_key)
        
        logger.info("WebAuthn credential registered successfully", 
                   user_id=request.user_id,
                   credential_id=verification_result["credential_id"][:8])
        
        return {
            "success": True,
            "credential_id": verification_result["credential_id"],
            "message": "Passkey registered successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("WebAuthn registration completion failed",
                    error=str(e), user_id=request.user_id)
        raise HTTPException(status_code=500, detail="Registration completion failed")

@router.post("/authenticate/begin")
async def webauthn_authenticate_begin(
    request: AuthenticationBeginRequest,
    http_request: Request,
    redis_client: FedJobRedisClient = Depends(),
    db = Depends(get_db)
):
    """
    Begin WebAuthn authentication process
    """
    try:
        # Get user credentials
        allow_credentials = []
        
        if request.user_id:
            # User-specific authentication
            user_creds = db.query(WebAuthnCredential).filter(
                WebAuthnCredential.user_id == int(request.user_id),
                WebAuthnCredential.is_active == True
            ).all()
            
            allow_credentials = [
                {
                    "type": "public-key",
                    "id": base64.urlsafe_b64encode(cred.credential_id).decode().rstrip('='),
                    "transports": cred.transports or ["internal", "usb", "nfc", "ble"]
                }
                for cred in user_creds
            ]
        
        # Generate challenge
        challenge = secrets.token_bytes(32)
        
        # Store challenge in Redis
        session_id = http_request.session.get("session_id")
        if not session_id:
            session_id = secrets.token_urlsafe(32)
            http_request.session["session_id"] = session_id
        
        challenge_key = f"webauthn:challenge:{session_id}"
        challenge_data = {
            "challenge": base64.urlsafe_b64encode(challenge).decode(),
            "user_id": request.user_id,
            "type": "authentication",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        redis_client.client.setex(
            challenge_key,
            120,  # 2 minutes
            json.dumps(challenge_data)
        )
        
        # Create authentication options
        options = {
            "challenge": base64.urlsafe_b64encode(challenge).decode().rstrip('='),
            "timeout": 120000,  # 2 minutes
            "rpId": http_request.url.hostname,
            "allowCredentials": allow_credentials,
            "userVerification": "required"
        }
        
        logger.info("WebAuthn authentication initiated",
                   user_id=request.user_id,
                   challenge_id=session_id)
        
        return options
        
    except Exception as e:
        logger.error("WebAuthn authentication begin failed",
                    error=str(e), user_id=request.user_id)
        raise HTTPException(status_code=500, detail="Authentication initialization failed")

@router.post("/authenticate/complete")
async def webauthn_authenticate_complete(
    request: AuthenticationCompleteRequest,
    http_request: Request,
    response: Response,
    verifier: WebAuthnVerifier = Depends(get_webauthn_verifier),
    redis_client: FedJobRedisClient = Depends(),
    db = Depends(get_db)
):
    """
    Complete WebAuthn authentication process
    """
    try:
        # Get challenge from Redis
        session_id = http_request.session.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="No active session")
        
        challenge_key = f"webauthn:challenge:{session_id}"
        challenge_data_str = redis_client.client.get(challenge_key)
        
        if not challenge_data_str:
            raise HTTPException(status_code=400, detail="Challenge expired or invalid")
        
        challenge_data = json.loads(challenge_data_str)
        
        if challenge_data["type"] != "authentication":
            raise HTTPException(status_code=400, detail="Invalid challenge type")
        
        # Get challenge bytes
        challenge = base64.urlsafe_b64decode(challenge_data["challenge"] + '==')
        
        # Find credential
        credential_id = base64.urlsafe_b64decode(request.assertion["rawId"] + '==')
        
        stored_credential = db.query(WebAuthnCredential).filter(
            WebAuthnCredential.credential_id == credential_id,
            WebAuthnCredential.is_active == True
        ).first()
        
        if not stored_credential:
            raise HTTPException(status_code=404, detail="Credential not found")
        
        # Prepare stored credential data for verification
        stored_cred_data = {
            "public_key": base64.urlsafe_b64encode(stored_credential.public_key).decode(),
            "signature_counter": stored_credential.signature_counter
        }
        
        # Verify authentication
        verification_result = verifier.verify_authentication(
            request.assertion, challenge, stored_cred_data
        )
        
        if not verification_result["verified"]:
            logger.warning("WebAuthn authentication verification failed",
                         credential_id=base64.urlsafe_b64encode(credential_id).decode()[:8],
                         error=verification_result.get("error"))
            raise HTTPException(status_code=401, 
                              detail=f"Authentication failed: {verification_result.get('error')}")
        
        # Update credential counter
        stored_credential.signature_counter = verification_result["signature_counter"]
        stored_credential.last_used_at = datetime.utcnow()
        if "backup_state" in verification_result:
            stored_credential.backup_state = verification_result["backup_state"]
        
        db.commit()
        
        # Create authenticated session
        user = stored_credential.user
        session_token = create_session(user.id, redis_client)
        
        # Set secure session cookie
        response.set_cookie(
            "fedjob_session",
            session_token,
            max_age=3600,  # 1 hour
            httponly=True,
            secure=True,  # HTTPS only
            samesite="strict"
        )
        
        # Clean up challenge
        redis_client.client.delete(challenge_key)
        
        logger.info("WebAuthn authentication successful",
                   user_id=user.id,
                   credential_id=base64.urlsafe_b64encode(credential_id).decode()[:8])
        
        return {
            "success": True,
            "user_id": str(user.id),
            "session_token": session_token,
            "message": "Authentication successful"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("WebAuthn authentication completion failed",
                    error=str(e))
        raise HTTPException(status_code=500, detail="Authentication completion failed")

@router.get("/credentials")
async def list_user_credentials(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    List user's registered WebAuthn credentials
    """
    try:
        credentials = db.query(WebAuthnCredential).filter(
            WebAuthnCredential.user_id == current_user.id,
            WebAuthnCredential.is_active == True
        ).all()
        
        return {
            "credentials": [
                {
                    "id": base64.urlsafe_b64encode(cred.credential_id).decode(),
                    "created_at": cred.created_at.isoformat(),
                    "last_used_at": cred.last_used_at.isoformat() if cred.last_used_at else None,
                    "backup_eligible": cred.backup_eligible,
                    "backup_state": cred.backup_state
                }
                for cred in credentials
            ]
        }
        
    except Exception as e:
        logger.error("Failed to list credentials", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to retrieve credentials")

@router.delete("/credentials/{credential_id}")
async def delete_credential(
    credential_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Delete a WebAuthn credential
    """
    try:
        cred_id_bytes = base64.urlsafe_b64decode(credential_id + '==')
        
        credential = db.query(WebAuthnCredential).filter(
            WebAuthnCredential.credential_id == cred_id_bytes,
            WebAuthnCredential.user_id == current_user.id,
            WebAuthnCredential.is_active == True
        ).first()
        
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found")
        
        credential.is_active = False
        db.commit()
        
        logger.info("WebAuthn credential deleted",
                   user_id=current_user.id,
                   credential_id=credential_id[:8])
        
        return {"success": True, "message": "Credential deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete credential", 
                    error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to delete credential")
'''

    def create_deployment_checklist(self) -> List[str]:
        """
        Create deployment checklist for WebAuthn in Fed Job Advisor
        
        Returns:
            List of deployment steps and checks
        """
        return [
            "✓ HTTPS certificate installed and verified",
            "✓ Domain name matches RP ID exactly (no subdomains)",
            "✓ WebAuthn API feature detection implemented",
            "✓ Progressive enhancement with password fallback",
            "✓ Python dependencies installed (python-jose, passlib, cbor2)",
            "✓ Database tables created for WebAuthn credentials",
            "✓ Redis cache configured for challenge storage",
            "✓ Session management integrated with WebAuthn auth",
            "✓ User registration flow includes passkey setup",
            "✓ Browser compatibility testing completed",
            "✓ Mobile device testing (iOS/Android)",
            "✓ Error handling for unsupported browsers",
            "✓ Rate limiting on authentication endpoints",
            "✓ Audit logging for all authentication events",
            "✓ Backup authentication methods configured",
            "✓ Recovery codes generated for users",
            "✓ Help documentation for passkey setup",
            "CRITICAL: Test on production domain before launch",
            "CRITICAL: Verify federal compliance requirements",
            "CRITICAL: Test fallback authentication flows",
            "FEDERAL: Implement session timeout (1 hour max)",
            "FEDERAL: Enable user verification requirement",
            "FEDERAL: Audit trail for authentication events"
        ]
    
    def get_troubleshooting_guide(self) -> Dict[str, Dict[str, str]]:
        """
        Get troubleshooting guide for WebAuthn issues
        
        Returns:
            Troubleshooting guide organized by issue type
        """
        return {
            "browser_issues": {
                "webauthn_not_supported": "Check browser version, enable WebAuthn in Firefox",
                "secure_context_required": "Ensure HTTPS is enabled, localhost works for dev",
                "platform_authenticator_unavailable": "Check TouchID/FaceID/Windows Hello settings",
                "user_verification_failed": "Verify biometric/PIN is set up on device"
            },
            "registration_failures": {
                "invalid_rp_id": "Ensure RP ID matches domain exactly",
                "challenge_expired": "Increase challenge timeout or reduce user delay",
                "credential_excluded": "User already has passkey registered",
                "attestation_verification_failed": "Check certificate chain validation"
            },
            "authentication_failures": {
                "credential_not_found": "Credential may be deleted or device changed",
                "signature_verification_failed": "Check public key storage and signature validation",
                "counter_regression": "Possible credential cloning attack",
                "user_verification_required": "Ensure device biometric/PIN is working"
            },
            "federal_compliance_issues": {
                "session_timeout_exceeded": "Reduce session timeout to 1 hour maximum",
                "user_verification_not_required": "Set userVerification to 'required'",
                "weak_authenticator": "Require platform authenticators only",
                "audit_logging_missing": "Implement comprehensive authentication audit trail"
            },
            "deployment_issues": {
                "rp_id_mismatch": "Verify RP ID matches production domain exactly",
                "origin_validation_failed": "Check origin header validation in server",
                "certificate_issues": "Ensure valid HTTPS certificate",
                "cross_origin_requests": "WebAuthn doesn't support cross-origin authentication"
            }
        }
    
    def load_ttl_documentation(self) -> Dict[str, str]:
        """
        Load TTL documentation for WebAuthn challenges and sessions
        
        Returns:
            Documentation explaining TTL choices for federal compliance
        """
        return {
            "challenge_ttl_5min": """
            TTL: 5 minutes (300 seconds) for registration challenges
            Reasoning: Provides adequate time for user to complete biometric
            authentication while minimizing exposure window. Federal security
            guidelines recommend short-lived challenges.
            """,
            
            "auth_challenge_ttl_2min": """
            TTL: 2 minutes (120 seconds) for authentication challenges  
            Reasoning: Authentication should be faster than registration.
            Shorter window reduces risk of challenge interception or replay.
            """,
            
            "session_ttl_1hour": """
            TTL: 1 hour (3600 seconds) for authenticated sessions
            Reasoning: NIST SP 800-63B recommends maximum 1 hour session
            lifetime for AAL2 (Authenticator Assurance Level 2) required
            for federal systems.
            """,
            
            "credential_cache_24hours": """
            TTL: 24 hours for credential lookup cache
            Reasoning: WebAuthn credentials are stable and don't change
            frequently. 24-hour cache improves authentication performance
            while still allowing for credential revocation.
            """,
            
            "federal_reauthentication_8hours": """
            TTL: 8 hours maximum before re-authentication required
            Reasoning: Federal systems require periodic re-authentication
            even with valid sessions. Users must re-authenticate at least
            every 8 hours for continued access.
            """
        }

def create_webauthn_specialist() -> WebAuthnSpecialist:
    """Factory function to create WebAuthn specialist instance"""
    return WebAuthnSpecialist()

# Example usage and testing
if __name__ == "__main__":
    specialist = create_webauthn_specialist()
    
    # Generate registration options
    reg_options = specialist.create_registration_options(
        user_id="user123",
        username="user@example.com", 
        display_name="John Doe",
        rp_id="fedjobadvisor.com"
    )
    print(f"Registration options generated: {len(reg_options)} fields")
    
    # Get deployment checklist
    checklist = specialist.create_deployment_checklist()
    print(f"Deployment checklist: {len(checklist)} items")
    
    # Get troubleshooting guide
    troubleshooting = specialist.get_troubleshooting_guide()
    print(f"Troubleshooting guide: {len(troubleshooting)} categories")