try:
    from .base import DataManagerStep
except ImportError:
    from steps.base import DataManagerStep


class ShiftSummaryHeaderStep(DataManagerStep):
    def apply(self, data, header):
        shift_summary = data.get("ShiftSummary") or {}

        pos_store_id = data.get("STORELOCATIONID")
        pos_begin_time = data.get("BEGINTIME")
        pos_end_time = data.get("ENDTIME")
        end_of_shift = bool(shift_summary.get("SHIFTDETAIL"))
        end_of_day = bool(shift_summary.get("DAYDETAIL"))
        terminal_id = data.get("_terminal_id")
        csu_shift_id = data.get("_csu_shift_id")

        header.BEGINTIME = self._dm.time_to_seconds(pos_begin_time or "")
        header.ENDTIME = self._dm.time_to_seconds(pos_end_time or "")
        header.ShiftId = csu_shift_id or ""
        header.TerminalId = terminal_id or ""
        header.OUN = self._dm.get_oun(pos_store_id)
        header.CsuBaseUrl = self._dm.get_csu_base_url(pos_store_id)
        header.endOfDay = int(end_of_day)
        header.endOfShift = int(end_of_shift or end_of_day)