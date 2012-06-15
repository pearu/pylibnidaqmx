"""
Routines for Getting/Setting physical channel attributes.
"""


from ctypes import byref, create_string_buffer
from libnidaqmx import uInt8, int32, bool32, float64, uInt32, \
                       CALL, default_buf_size


def get_ai_terminal_config_bits(channel):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_AI_TermCfgs ***
   Uses bits from enum TerminalConfigurationBits
  """
  channel = str(channel)
  bits = int32(0)
  CALL('GetPhysicalChanAITermCfgs', channel, byref(bits))
  return bits.value


def get_ao_terminal_config_bits(channel):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_AO_TermCfgs ***
   Uses bits TerminalConfigurationBits
  """
  channel = str(channel)
  bits = int32(0)
  CALL('GetPhysicalChanAOTermCfgs', channel, byref(bits));
  return bits.value


def get_ao_manual_control_enable( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_AO_ManualControlEnable ***
  """
  enable = bool32(0)
  CALL('GetPhysicalChanAOManualControlEnable', channel, byref(enable))
  return bool( enable.value )


def set_ao_manual_control_enable( channel, enable ):
  enable = bool32(enable)
  CALL('SetPhysicalChanAOManualControlEnable', channel, byref(enable))


def reset_ao_manual_control_enable( channel ):
  CALL('ResetPhysicalChanAOManualControlEnable', channel);


def get_ao_manual_control_ampl( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_AO_ManualControlAmplitude ***
  """
  amp = float64(0)
  CALL('GetPhysicalChanAOManualControlAmplitude', channel, byref(amp))
  return amp.value


def get_ao_manual_control_freq( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_AO_ManualControlFreq ***
  """
  freq = float64(0)
  CALL('GetPhysicalChanAOManualControlFreq', channel, byref(freq))
  return freq.value


def get_di_port_width( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_DI_PortWidth ***
  """
  width = uInt32(0)
  CALL('GetPhysicalChanDIPortWidth', channel, byref(width))
  return width.value


def get_di_sample_clock_supported( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_DI_SampClkSupported ***
  """
  supported = bool32(0)
  CALL('GetPhysicalChanDISampClkSupported', channel, byref(supported))
  return bool( supported.value )


def get_di_change_detection_supported( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_DI_ChangeDetectSupported ***
  """
  supported = bool32(0)
  CALL('GetPhysicalChanDIChangeDetectSupported', channel, byref(supported))
  return bool( supported.value )


def get_do_port_width( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_DO_PortWidth ***
  """
  width= uInt32(0)
  CALL('GetPhysicalChanDOPortWidth', channel, byref(width))
  return width.value


def get_do_sample_clock_supported( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_DO_SampClkSupported ***
  """
  supported = bool32(0)
  CALL('GetPhysicalChanDOSampClkSupported', channel, byref(supported))
  return bool( supported.value )


def get_teds_mfgId( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_MfgID ***
  """
  mfgID = uInt32(0)
  CALL('GetPhysicalChanTEDSMfgID', channel, byref(mfgID))
  return mfgID.value


def get_teds_model( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_ModelNum ***
  """
  model = uInt32(0)
  CALL('GetPhysicalChanTEDSModelNum', channel, byref(model))
  return model.value


def get_teds_serial( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_SerialNum ***
  """
  serial = uInt32(0)
  CALL('GetPhysicalChanTEDSSerialNum', channel, byref(serial))
  return serial.value


def get_teds_version( channel ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_VersionNum ***
  """
  version = uInt32(0)
  CALL('GetPhysicalChanTEDSVersionNum', channel, byref(version))
  return version.value


def get_teds_versionletter( channel, buf_size=None ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_VersionLetter ***
  """
  if buf_size is None:
    buf_size = default_buf_size
  buf = create_string_buffer('\000' * buf_size)
  CALL('GetPhysicalChanTEDSVersionLetter', channel, byref(buf), buf_size)
  return buf.value


def get_teds_bit_stream( channel, buf_size=None ): 
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_BitStream ***
  """
  if buf_size is None:
    buf_size = default_buf_size
  buf = (uInt8*buf_size)()
  CALL('GetPhysicalChanTEDSBitStream', channel, byref(buf), buf_size)
  return buf[:]


def get_teds_template_ids( channel, buf_size=None ):
  """
  *** Set/Get functions for DAQmx_PhysicalChan_TEDS_TemplateIDs ***
  """
  if buf_size is None:
    buf_size = default_buf_size
  buf = (uInt32*buf_size)()
  CALL('GetPhysicalChanTEDSTemplateIDs', channel, byref(buf), buf_size)
  return buf[:]
